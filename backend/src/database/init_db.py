from .connection import create_db_and_tables


def initialize_database():
    """
    Initialize the database by creating all required tables.

    This function should be called during application startup to ensure
    that all database tables exist.
    """
    create_db_and_tables()
    print("Database tables created successfully!")