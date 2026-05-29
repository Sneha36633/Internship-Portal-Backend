# This file makes the 'models' folder a Python package and exposes its contents.

# Import the model classes so they can be discovered by other parts of the application,
# especially by SQLAlchemy when creating tables.
from .user_model import User
from .skill_model import Skill
from .company_model import Company
from .internship_model import Internship
from .recommendation_model import Recommendation

