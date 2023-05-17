from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,

)
from sqlalchemy.orm import relationship
from drive_server.app.database.sqlalchemy_model.database_sqlalchemy import Base









class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    registration_time = Column(DateTime, server_default=func.now())



class UserSession(Base):
    __tablename__ = "user_session"

    id = Column(Integer, primary_key=True)
    id_session = Column(String(100), nullable=False, unique=True)
    create_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User, lazy="joined")

