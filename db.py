from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("mysql+pymysql://root:aA123456@localhost:3306/taro4")
session = Session(bind=engine)
Base = declarative_base()

class Users(Base):
        __tablename__ = 'users'
        id = Column(Integer(), primary_key=True)
        first_name = Column(String(100), nullable=False)
        last_name = Column(String(100), nullable=True)
        surname = Column(String(50), nullable=True)
        telegram = Column(String(200), nullable=True)
        whatsapp = Column(String(200), nullable=True)
        email = Column(String(200), nullable=False)
        created_on = Column(DateTime(), default=datetime.now)
        updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
        rule = Column(Integer(), nullable=True)
        block = Column(Integer(), nullable=True)
        password = Column(String(100), nullable=True)
        orders = relationship("Order", backref='users')
        
class Item(Base):
        __tablename__ = 'items'
        id = Column(Integer(), primary_key=True)
        name = Column(String(200), nullable=False)
        cost_price =  Column(Numeric(10, 2), nullable=False)
        selling_price = Column(Numeric(10, 2),  nullable=False)
        quantity = Column(Integer())


class Order(Base):
        __tablename__ = 'orders'
        id = Column(Integer(), primary_key=True)
        customer_id = Column(Integer(), ForeignKey('users.id'))
        date_placed = Column(DateTime(), default=datetime.now)
        line_items = relationship("OrderLine", backref='order')
        

class OrderLine(Base):
        __tablename__ = 'order_lines'
        id =  Column(Integer(), primary_key=True)
        order_id = Column(Integer(), ForeignKey('orders.id'))
        item_id = Column(Integer(), ForeignKey('items.id'))
        quantity = Column(SmallInteger())
        item = relationship("Item")

def create_db():
    Base.metadata.create_all(engine)
    user1 = Users(
            first_name = "Екатерина", 
            last_name = "Ферреро", 
            surname = "Олеговна", 
            telegram = "antence73@mail.com",
            whatsapp = "antence73@mail.com",
            email = "antence73@mail.com",
            rule = 1,
            block = 0,
            password = "12345678",)
        
    user2 = Users(
            first_name = "Андрей", 
            last_name = "Ферреро", 
            surname = "Олеговна", 
            telegram = "antence73@mail.com",
            whatsapp = "antence73@mail.com",
            email = "aovakur@yandex.ru",
            rule = 1,
            block = 0,
            password = "12345678",
            )
    session.add_all([user1,user2])
    session.commit()

def open_session(): 
    return session