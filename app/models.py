#every model represnts a table in our ddbb
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

#here we are creting another table to keep the old one and the new let`s name it posts_orm

class PostORM(Base):
    __tablename__="posts_orm"

    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False) 
    published=Column(Boolean, server_default='TRUE')
    created_at=Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    