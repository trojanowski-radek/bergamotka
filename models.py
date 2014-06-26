#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker, )

from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.orm import relationship, deferred, backref
from sqlalchemy.types import *
from sqlalchemy import *

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base(metadata=MetaData(schema='bergamotka'))

from datetime import datetime, timedelta

from pyramid.security import Allow
from pyramid.security import Everyone


class RootFactory(object):
    """
    Pyramid being called on every request sent to the application.security

    __acl__ - (access control list) maps users permissions with views restrictions
    """
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'permission:ADMIN', 'admin')]

    def __init__(self, request):
        pass


class Users(Base):
    """
        This table represents list of users
    """
    
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    fname = Column(Text, nullable=False)
    lname = Column(Text, nullable=False, index=True)
    email = Column(Text, nullable=False)
    permission = Column(Text, nullable=False, default='VIEW')
    pwd = Column(Text, nullable=False)

    def __init__(self, fname, lname, email, permission, pwd):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.permission = permission
        self.pwd = pwd


class Reservations(Base):
    """
        This table represents reservations done by users
    """
    
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Text, index=True, nullable=False)
    date_start = Column(DateTime, nullable=False, default=datetime.now())
    date_end = Column(DateTime, nullable=False, default=datetime.now() + timedelta(hours=1))
    title = Column(Text, nullable=False, default='Reservation')
    phone = Column(Text, nullable=False)

    def __init__(self, user, date_start, date_end, title, phone):
        self.user = user
        self.date_start = date_start
        self.date_end = date_end
        self.title = title
        self.phone = phone


class Events(Base):
    """
        This table represents events created by company
    """
    
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Text, index=True, nullable=True)
    date_start = Column(DateTime, nullable=False, default=datetime.now())
    date_end = Column(DateTime, nullable=False, default=datetime.now() + timedelta(hours=1))
    title = Column(Text, nullable=False, default='Reservation')

    def __init__(self, user, date_start, date_end, title):
        self.user = user
        self.date_start = date_start
        self.date_end = date_end
        self.title = title


class News(Base):
    """
        This table represents list of added news
    """
    
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    added = Column(DateTime, nullable=False, default=datetime.now())
    content = Column(Text, nullable=True)
    image = Column(Text, nullable=True)

    def __init__(self, title, added, content, image):
        self.title = title
        self.added = added
        self.content = content
        self.image = image


class Dishes(Base):
    """This table represents list of dishes in menu"""

    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    ingredients = Column(Text, nullable=True)
    price = Column(Text, nullable=True)
    type = Column(Text, nullable=False)
    image = Column(Text, nullable=True)

    def __init__(self, title, ingredients, price, type, image):
        self.title = title
        self.ingredients = ingredients
        self.price = price
        self.type = type
        self.image = image