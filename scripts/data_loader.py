import pandas as pd
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the project root to the Python path to allow imports from the 'app' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary components from your FastAPI application
from app.config.database import engine
from app.models import user_model, skill_model, company_model, internship_model
from app.crud import user_crud, skill_crud, company_crud, internship_crud
from app.schemas import user_schemas, skill_schemas, company_schemas, internship_schemas

# --- Database Session Setup ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_data():
    """
    Main function to read CSVs and load the data into the database.
    """
    db = SessionLocal()
    print("✅ Database session started.")

    try:
        # --- 1. Load User Profiles and their Skills ---
        print("\n🔄 Processing profiles.csv...")
        profiles_df = pd.read_csv('temp/profiles.csv')

        for _, row in profiles_df.iterrows():
            user_id_from_csv = row['user_id']
            user_skills_from_csv = row['skills']
            
            user_name_from_csv = f"User {user_id_from_csv}"
            user_email_from_csv = f"user_{user_id_from_csv}@example.com"

            existing_user = user_crud.get_user_by_email(db, email=user_email_from_csv)
            
            if not existing_user:
                user_data = user_schemas.UserCreate(
                    full_name=user_name_from_csv,
                    email=user_email_from_csv,
                    password="password123"
                )
                user = user_crud.create_user(db, user=user_data)
                print(f"  - Created new user: {user.email}")
            else:
                user = existing_user

            if pd.notna(user_skills_from_csv) and isinstance(user_skills_from_csv, str):
                skill_names = [skill.strip() for skill in user_skills_from_csv.split(',')]
                
                for skill_name in skill_names:
                    existing_skill = skill_crud.get_skill_by_name(db, name=skill_name)
                    if not existing_skill:
                        skill_data = skill_schemas.SkillCreate(name=skill_name)
                        skill = skill_crud.create_skill(db, skill=skill_data)
                        print(f"    - Created new skill: {skill.name}")
                    else:
                        skill = existing_skill
                    
                    if skill not in user.skills:
                        user.skills.append(skill)
        
        db.commit()
        print("✅ Successfully loaded profiles and user skills.")

        # --- 2. Load Companies and Internships ---
        print("\n🔄 Processing opportunities.csv...")
        opportunities_df = pd.read_csv('temp/opportunities.csv')

        for _, row in opportunities_df.iterrows():
            # !! IMPORTANT !! Please update this line with the actual column name for the company from your CSV
            company_name_from_csv = "Default Company" # e.g., row['company_name'] 
            
            # Convert the integer from 'job_id' to a string for the title
            opportunity_title_from_csv = str(row['job_id']) # <-- FIX IS HERE
            
            # Using 'requirements' for both description and skills, as it's the most descriptive field
            description_from_csv = row['requirements']
            required_skills_from_csv = row['requirements']

            existing_company = db.query(company_model.Company).filter(company_model.Company.name == company_name_from_csv).first()

            if not existing_company:
                company_data = company_schemas.CompanyCreate(name=company_name_from_csv)
                company = company_crud.create_company(db, company=company_data)
                print(f"  - Created new company: {company.name}")
            else:
                company = existing_company

            skill_ids = []
            if pd.notna(required_skills_from_csv) and isinstance(required_skills_from_csv, str):
                skill_names = [skill.strip() for skill in required_skills_from_csv.split(',')]
                for skill_name in skill_names:
                    existing_skill = skill_crud.get_skill_by_name(db, name=skill_name)
                    if not existing_skill:
                        skill_data = skill_schemas.SkillCreate(name=skill_name)
                        skill = skill_crud.create_skill(db, skill=skill_data)
                        print(f"    - Created new skill: {skill.name}")
                    else:
                        skill = existing_skill
                    skill_ids.append(skill.id)
            
            internship_data = internship_schemas.InternshipCreate(
                title=opportunity_title_from_csv,
                description=description_from_csv,
                company_id=company.id,
                skill_ids=skill_ids
            )
            internship_crud.create_internship(db, internship=internship_data)
            print(f"  - Created internship: {internship_data.title}")

        print("✅ Successfully loaded opportunities and internship skills.")

    except KeyError as e:
        print(f"\n❌ An error occurred: A column was not found in your CSV file. Please check for a column named: {e}")
        db.rollback()
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
        print("\n✅ Database session closed.")

if __name__ == "__main__":
    load_data()

