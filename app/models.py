import datetime
from enum import unique
from sqlalchemy import Column, Integer
from app import db

from sqlalchemy import *
from sqlalchemy.orm import relationship

class Call(db.Model):
    __tablename__ = "calls"
    
    id = Column(Integer, primary_key=True)
    
    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="calls")
    
    userTo = Column(String(320))
    
    APICall = Column(String(100)) #Not sure how to define the in
    
    timeCalled = Column(DateTime(timezone=True), server_default=func.now())

    userAuth = Column(Boolean, nullable = False)
    
class User(db.Model):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    
    email = Column(String(320), nullable = False, unique = True)
    
    username = Column(String(100), nullable = False, unique = True)
    
    password = Column(String(100), nullable = False)
    
    calls = relationship("Call", order_by=Call.id, back_populates="user")