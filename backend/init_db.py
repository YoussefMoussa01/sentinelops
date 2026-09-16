"""Database initialization script."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine
# Import models so SQLAlchemy registers every table before create_all.
from app import models  # noqa: F401

def init_db():
    """Initialize database and create all tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
