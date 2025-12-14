from sqlmodel import SQLModel, create_engine, Session

# Use a file-based SQLite database for the actual application
sqlite_file_name = "sweets.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread is only needed for SQLite
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    # This will be called on startup to create the DB and tables if they don't exist
    import models  # noqa
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
