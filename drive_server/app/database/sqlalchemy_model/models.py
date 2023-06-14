import uuid
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
from sqlalchemy.dialects.postgresql import UUID








class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    registration_time = Column(DateTime, server_default=func.now())
    user_token = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4,index=False) # при миграции может быть ошибка добавить команду CREATE EXTENSION IF NOT EXISTS "uuid-ossp";



class UserSession(Base):
    __tablename__ = "user_session"

    id = Column(Integer, primary_key=True)
    id_session = Column(String(100), nullable=False, unique=True)
    create_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User, lazy="joined")

