from sqlmodel import SQLModel, create_engine, Session

# Local SQLite database file: codesentinel.db
sqlite_file_name = "codesentinel.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args={"check_same_thread": False} is required only for SQLite
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Creates database tables automatically when app starts."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency that provides a database session to route handlers."""
    with Session(engine) as session:
        yield session