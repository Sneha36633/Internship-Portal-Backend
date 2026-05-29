import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import database components
from app.config.database import engine
from app.models import User, Internship, Recommendation

# --- Database Session Setup ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

print("✅ Database session started.")
print("✅ This may take a moment as the AI model is loaded...")

try:
    # -------------------------------
    # 1. Load data FROM THE DATABASE (replaces pd.read_csv)
    # -------------------------------
    print("\n🔄 Fetching data from the database...")
    
    # Fetch all users and their skills
    users = db.query(User).all()
    profiles_data = []
    for user in users:
        profiles_data.append({
            'user_id': user.id, # Using the actual database ID
            'skills': ', '.join([skill.name for skill in user.skills])
        })
    profiles_df = pd.DataFrame(profiles_data)

    # Fetch all internships and their requirements
    internships = db.query(Internship).all()
    opportunities_data = []
    for internship in internships:
        opportunities_data.append({
            'internship_id': internship.id, # Using the actual database ID
            'requirements': internship.description
        })
    opportunities_df = pd.DataFrame(opportunities_data)

    print(f"  - Loaded {len(profiles_df)} user profiles and {len(opportunities_df)} opportunities.")

    # -------------------------------
    # 2. AI Model and Embedding (Your original logic)
    # -------------------------------
    print("\n🧠 Encoding skills and requirements with AI model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    profile_embeddings = model.encode(profiles_df["skills"].tolist())
    opportunity_embeddings = model.encode(opportunities_df["requirements"].tolist())
    print("  - Encoding complete.")

    # -------------------------------
    # 3. Match each profile with opportunities (Your original logic)
    # -------------------------------
    print("\n🤝 Matching profiles to opportunities...")
    new_recommendations = []

    for i, profile in profiles_df.iterrows():
        # Calculate cosine similarities
        sims = cosine_similarity([profile_embeddings[i]], opportunity_embeddings)[0]
        
        for j, opp in opportunities_df.iterrows():
            score = sims[j]
            
            # We only create a recommendation if the score is above a certain threshold
            if score > 0.1: # You can adjust this threshold
                recommendation = Recommendation(
                    user_id=profile["user_id"],
                    internship_id=opp["internship_id"], # Using the correct database ID
                    match_score=round(float(score), 2)
                )
                new_recommendations.append(recommendation)
    print("  - Matching complete.")
    
    # -------------------------------
    # 4. Save results TO THE DATABASE (replaces df.to_csv)
    # -------------------------------
    print("\n💾 Saving results to the database...")
    # First, clear any old recommendations
    db.query(Recommendation).delete()
    db.commit()

    # Now, add all the new recommendations
    if new_recommendations:
        db.add_all(new_recommendations)
        db.commit()
        print(f"  - Successfully saved {len(new_recommendations)} recommendations.")
    else:
        print("  - No new recommendations to save.")

except Exception as e:
    print(f"\n❌ An error occurred: {e}")
    db.rollback()
finally:
    db.close()
    print("\n✅ Database session closed.")

