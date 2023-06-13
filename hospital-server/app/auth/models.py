from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.configuration import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    groups = relationship('Groups', secondary='user_groups')


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship('User', secondary='user_groups')


class UserGroups(Base):
    __tablename__ = 'user_groups'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)