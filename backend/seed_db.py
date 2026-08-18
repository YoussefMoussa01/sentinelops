"""Database seeding script - creates initial test data."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User
from app.core.security import hash_password
import uuid

def seed_db():
    """Create initial test users."""
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("Test users already exist, skipping seed.")
            return
        
        # Create admin user
        admin = User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@sentinelops.local",
            password_hash=hash_password("AdminPassword123!"),
            is_active=True,
        )
        db.add(admin)
        
        # Create test investigator
        investigator = User(
            id=str(uuid.uuid4()),
            username="investigator",
            email="investigator@sentinelops.local",
            password_hash=hash_password("InvestigatorPassword123!"),
            is_active=True,
        )
        db.add(investigator)
        
        db.commit()
        print("Database seeded successfully!")
        print("  - admin / AdminPassword123!")
        print("  - investigator / InvestigatorPassword123!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
