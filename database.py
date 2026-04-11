from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///app.db')


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Ensure SQLite enforces foreign-key constraints for cascades."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    __import__("app.models.user")
    __import__("app.models.courses")
    __import__("app.models.enrollment")
    __import__("app.models.student")
    __import__("app.models.instructor")
    Base.metadata.create_all(bind=engine)
