from sqlalchemy import create_engine

def get_engine():
    """
    Creates and returns a SQLAlchemy engine for MySQL connection.
    Update credentials if needed.
    """
    engine = create_engine(
        "mysql+mysqlconnector://<<your_username>>:<<your_password>>@localhost/<<your_database_name>>",
        pool_pre_ping=True  # ensures connection validity before use
    )
    return engine
