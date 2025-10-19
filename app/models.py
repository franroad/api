#every model represnts a table in our ddbb
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


#here we are creting another table to keep the old one and the new let`s name it posts_orm

class PostORM(Base):
    __tablename__="posts_orm"

    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False) 
    published=Column(Boolean, server_default='TRUE')
    created_at=Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False) 
    op = relationship ("Users") #pydantic lee la constraint join de sql alchemy (models.py)

class Users(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, nullable= False)#tiene el autoincrement habilitado por defecto (autoincrement=True)
    email= Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Code(Base):
    __tablename__="code"
    id=Column(Integer, primary_key=True, nullable= False)
    code=Column(String,nullable=False)
    email= Column(String, nullable=False)
    expires_at=Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), primary_key=True)
    post_id=Column(Integer,ForeignKey("posts_orm.id",ondelete="CASCADE"),primary_key=True)

    
