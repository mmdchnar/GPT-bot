from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from config import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class GetDB:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        if isinstance(exc_value, SQLAlchemyError):
            self.db.rollback()

        self.db.close()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    username = Column(String(64))
    last_used = Column(DateTime)
    is_ban = Column(Boolean, default=False)

    @staticmethod
    def update_or_create(db: Session, userid, name=None, username=None):
        user = db.get(User, userid)
        if user:
            if name:
                user.name = name
            if username:
                user.username = username or ''
        else:
            user = User(id=userid, name=name, username=username or '')
            db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def set_last_used(self, db: Session):
        self.last_used = datetime.now()
        db.commit()
        db.refresh(self)
