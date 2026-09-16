"""Database seeding script - creates initial test data."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User
from app.core.security import hash_password
from app.core.config import get_settings
import uuid
import os

def seed_db():
    """Create optional local development users from environment variables."""
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("Test users already exist, skipping seed.")
            return
        
        settings = get_settings()
        admin_password = os.getenv("SEED_ADMIN_PASSWORD") or settings.SUPER_ADMIN_PASSWORD
        investigator_password = os.getenv("SEED_INVESTIGATOR_PASSWORD")
        if not admin_password or not investigator_password:
            raise RuntimeError(
                "Set SEED_ADMIN_PASSWORD (or SUPER_ADMIN_PASSWORD) and "
                "SEED_INVESTIGATOR_PASSWORD before running seed_db.py"
            )

        admin = User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@sentinelops.local",
            password_hash=hash_password(admin_password),
            is_active=True,
            role="SUPER_ADMIN",
        )
        db.add(admin)
        
        # Create test investigator
        investigator = User(
            id=str(uuid.uuid4()),
            username="investigator",
            email="investigator@sentinelops.local",
            password_hash=hash_password(investigator_password),
            is_active=True,
            role="INVESTIGATOR",
        )
        db.add(investigator)
        
        db.commit()
        print("Database seeded successfully!")
        print("  - admin account created")
        print("  - investigator account created")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
