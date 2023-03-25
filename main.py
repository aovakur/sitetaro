# -*- coding: utf8 -*-
# coding: utf8
# coding=utf8

from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import Session, sessionmaker
import logging
from flask import Flask,flash,request,redirect,send_file, jsonify, abort, Markup,render_template,session as ses
from sqlalchemy import *
import numbers
import base64
import random
from random import randint
import codecs
import html
from base64 import b64encode
from functools import wraps
from flask_paginate import *
import socket
from requests import get
import asyncio

app = Flask(__name__)

'''engine = create_engine("mysql+pymysql://root:16Andrew93vak@localhost:3306/taro53")'''
engine = create_engine("mysql+pymysql://root:aA123456@localhost:3306/taro51")
session = Session(bind=engine)
Base = declarative_base()

class Logger(Base):
        __tablename__ = 'logging'
        id=Column('id', Integer(), nullable=False, unique=True, primary_key=True)
        request=Column('request', String(50), nullable=False)
        name = Column('name', String(50), nullable=False)
        operation = Column('operation', String(200),  nullable=False)
        ip = Column('ip',String(20), nullable = True)
        error = Column('error', String(200),  nullable=False)
        created_on = Column('created_on', DateTime(), default=datetime.now)

class Pages(Base):
        __tablename__ = 'pages'
        pages_id = Column(Integer(), primary_key=True)
        url = Column('name', String(100), nullable=False)
        title = Column('title', String(100), nullable = False)
        meta = Column('meta', String(100), nullable = True)
        author = Column('author', String(100), nullable=False)
        text = Column('description', Text, nullable=False)
        created_on = Column('created_on', DateTime(), default=datetime.now)

class Curses(Base):
        __tablename__ = 'curses'
        curses_id = Column(Integer(), primary_key=True)
        name = Column('name', String(100), nullable=False)
        url = Column('url', String(100), nullable=False)
        author = Column('author', String(100), nullable=False)
        description = Column('description', Text(), nullable=False)
        picture = Column('picture', String(50), nullable=False,default="")
        cost = Column('cost', Integer(), nullable=False,default=0)
        created_on = Column('created_on', DateTime(), default=datetime.now)
        lessons = Column('lessons', String(200), default="")

class Lessons(Base):
        __tablename__ = 'lessons'
        lessons_id = Column(Integer(), primary_key=True)
        curse = Column('curse', Integer(), ForeignKey('curses.curses_id'))
        name = Column('name', String(250), default="")
        description = Column('description', String(200), nullable=False)
        lesson = Column(Integer(), default="")
        homework = Column(Text(), default="")
        data = Column(Text(), default="")
        created_on = Column('created_on', DateTime(), default=datetime.now)

class User_role(Base):
        __tablename__ = 'users_role'
        id = Column(Integer(),primary_key=True)
        name = Column(String(50), nullable = False)      

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
class Order(Base):
        __tablename__ = 'orders'
        id = Column(Integer(), primary_key=True)
        user_id = Column(Integer(), ForeignKey('users.id'), nullable=True)
        curs_id = Column(Integer(), nullable=True)
        date_create = Column(DateTime(), default=datetime.now)
        payment = Column(String(50),nullable=True)
        payment_type = Column(String(50),nullable=True)
        payment_code = Column(String(50),nullable=True)
        payment_date = Column(DateTime(), nullable=True)
        date_expired = Column(DateTime(), nullable = True)
class Payment(Base):
       __tablename__ = 'payment'
       id = Column(Integer(), primary_key = True)
       name = Column(String(50), nullable = False)

class Payment_type(Base):
        __tablename__ = 'payment_type'
        id = Column (Integer(), primary_key = True)
        name = Column (String(50), nullable = False)
     
class Settings_site(Base):
        __tablename__ = 'settings_site'
        id =  Column(Integer(), primary_key=True)
        site_name = Column(String(200), nullable=False)
        site_name_eng = Column(String(200), nullable=False)
        email_admin = Column(String(200), nullable=False)
        email_smtp = Column(String(200), nullable=False)
        description = Column(String(200), nullable=False)
        meta_tag = Column(String(200), nullable=False)

class Onlinetaro(Base):
        __tablename__ = 'onlinetaro'
        id =  Column(Integer(), primary_key=True)
        carta = Column(String(200), nullable=False)
        eng = Column(String(20),nullable=False)
        type_carta = Column(String(200), nullable=False)
        type_carta_eng = Column(String(200), nullable=False)
        img = Column(String(200), nullable=False)
        graph_simphol = Column(Text, nullable=False)
        name_carta = Column(String(200), default="")
        name2_carta = Column(String(200), default="")
        description_cart = Column(Text, default="")
        general_carta = Column(Text, default="")
        psih_har = Column(Text, default="")
        zodiak = Column(Text, default="")
        starhie_arkan= Column(Text, default="")
        mechi = Column(Text, default="")
        pentakl = Column(Text, default="")
        zhezl = Column(Text, default="")
        kubki = Column(Text, default="")
        busnes1 = Column(Text, default="")
        busnes2 = Column(Text, default="")
        love1 = Column(Text, default="")
        love2 = Column(Text, default="")
        yesno = Column(Text, default="")
    

def create_db():
    Base.metadata.create_all(engine)

    role1 = User_role(
        name = "Администратор")
    role2 = User_role(
        name = "Модератор")
    role3 = User_role(
        name = "Участник")
    role4 = User_role(
        name = "Бесплатный доступ")
    role5 = User_role(
        name = "Зарегистрированный")

    pay1 = Payment(
        name = "Оплачен",)
    pay2 = Payment(
        name = "Не оплачен",)
    pay3 = Payment(
        name = "Подтвержден",)

    paytype1 = Payment_type(
        name = "Безнал на р/c",)
    paytype2 = Payment_type(
        name = "Наличные",)
    paytype3 = Payment_type(
        name = "Онлайн",)
    paytype4 = Payment_type(
        name = "Перевод СБП",)
    paytype5 = Payment_type(
        name = "Перевод",)

    settings_site = Settings_site(
            site_name = "Екатерина Ферреро Таролог", 
            site_name_eng = "tarolog", 
            email_admin = "aovakur@yandex", 
            email_smtp = "smtp.aovakur@yandex",
            description = "Услуги таролога",
            meta_tag = "Услуги таролога 2",)
    user1 = Users(
            first_name = "Екатерина", 
            last_name = "Ферреро", 
            surname = "Олеговна", 
            telegram = "antence73@mail.com",
            whatsapp = "antence73@mail.com",
            email = "antence73@mail.com",
            rule = 1,
            block = 0,
            password = "YUExMjM0NTY=",)
    user2 = Users(
            first_name = "Андрей", 
            last_name = "Вакурин", 
            surname = "Олегович", 
            telegram = "aovakur",
            whatsapp = "8965395195",
            email = "aovakur@yandex.ru",
            rule = 1,
            block = 0,
            password = "YUExMjM0NTY=",
            )
    curs1 = Curses(
            name = "Первый курс", 
            url = "petrov",
            author="Иванов",
            description = "description", 
            picture = "picture",
            cost = 25000,
            )
    les1 = Lessons(
            curse = "1", 
            name = "petrov",
            description="Иванов",
            lesson = 1, 
            homework = "picture",
            data = "picture",
            )

    les2 = Lessons(
            curse = "1", 
            name = "petrov",
            description="Иванов",
            lesson = 2, 
            homework = "picture",
            data = "picture",
            )

    session.add_all([user1,user2,settings_site])
    session.add_all([role1,role2,role3,role4,role5])
    session.add_all([pay1,pay2,pay3])
    session.add_all([paytype1,paytype2,paytype3,paytype4,paytype5])
    session.commit()

class OnlineTaro:
   
    @staticmethod
    async def cardday ():
        session1 = Session(bind=engine)
        random = randint(1, 28)
        context = session1.query(Onlinetaro.carta,Onlinetaro.img,Onlinetaro.busnes1).filter(Onlinetaro.id == random).first()
        return context

    @staticmethod
    async def getrandomcard():
        session1 = Session(bind=engine)
        random = randint(1, 78)
        context = session1.query(Onlinetaro.carta,Onlinetaro.graph_simphol,Onlinetaro.img,Onlinetaro.general_carta).filter(Onlinetaro.id == random).first()
        return context

    @staticmethod
    async def generated_card_func(item):
        generated_card = []
        select_card=[]
        count=session.query(Onlinetaro).count()
        for i in range(count): 
            select_card.append(i+1)
        for i in range(item):       
            random_value = random.choice(select_card)
            select_card.remove(random_value)
            generated_card.append(random_value) 
        return generated_card
    
    @staticmethod
    async def generated_card_position():
        random_value =[0,1]
        rotation = random.choice(random_value)
        if (rotation == 0):
            return "0deg"
        if (rotation == 1):
            return "180deg"

    @staticmethod
    async def generated_card_info(item, generated_card):
        context = {}
        for i in range (0,item):
            number_card = "card"+str(i)
            card = session.query(Onlinetaro).filter(Onlinetaro.id == generated_card[i]).first()
            context[number_card] = {
            'cart_id':card.id,
            'carta':card.carta,
            'eng':card.eng,
            'type_carta':card.type_carta,
            'type_carta_eng':card.type_carta_eng,
            'img':card.img,
            'graph_simphol':card.graph_simphol,
            'name_carta':card.name_carta,
            'name2_carta':card.name2_carta ,
            'description_cart':card.description_cart,
            'general_carta':card.general_carta,
            'psih_har':card.psih_har,
            'zodiak':card.zodiak,
            'busnes1':card.busnes1,
            'busnes2':card.busnes2,
            'love1':card.love1,
            'love2':card.love2,
            'yesno':card.yesno}
       
        return context          

rubashka = "http://centr-taro-ferre.ru/static/taro/rubashka.jpg"
param = 0
logger_info = None
header ={}
userprofile = None
registration = None
superUser = None


class Logger_info:
    @staticmethod
    def logger(request,operation,name, error="0"):
        with engine.connect() as conn:
            transaction = conn.begin()
            try:
                try:
                    ip = get('https://api.ipify.org').content.decode('utf8')
                except: 
                    ip = "unknown"
                session.add(Logger(request=request,name = name, operation = operation, ip=ip, error = error))
                session.commit()
                transaction.commit()
            except Exception as E:
                app.logger.info(E)
                transaction.rollback()

class Settings:
    def getglobalsettings(): 
        setting = session.query(Settings_site).first()
        setting_title = setting.site_name
        setting_title_eng = setting.site_name_eng
        setting_discription = setting.description
        setting_meta = setting.meta_tag
        setting_email_admin = setting.email_admin
        setting_email_smtp = setting.email_smtp
        global header
        header = {'site_name':setting_title,
        'site_name_eng':setting_title_eng,
        'description':setting_discription , 
        'meta_tag': setting_meta, 
        'email_admin':setting_email_admin,
        'email_smtp' : setting_email_smtp }

class User: 
    def __init__(self):
        self.user_curs = {}
        self.first_name = ""
        self.last_name = ""
        self.surname = ""
        self.telegram = ""
        self.email = ""
        self.rule = ""
        self.id = ""

    def getcurrentuser():
        pass

class SuperUser(User):
    def __init__(self):
        self.cursdelerrorcount = 0
        self.cursdelerror = 0
        super().__init__()

class Registration:
    def __init__(self):
        self.curs_list = []
        self.curs_count = 0
        self.discont = 10
        
    def getlencurs(self):
        return self.curs_list

    def getcurse(self):
        curses = session.query(Curses).filter(Curses.curses_id.in_(ses['reg'])).all()
        return curses 

    def getcast(self):
        try:
            curses = session.query(Curses).filter(Curses.curses_id.in_(ses['reg'])).all()
            temp = 0
            for cur in curses:  
                temp = cur.cost + temp
            ses['cost'] = temp

            if len(ses['reg'])>=2:
                ses['discont']="10%"
                ses['total_cost'] = int(90*int(ses['cost'])/100)
        except: 
            abort(404)

class Header():
    pass

def authorization_verification(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        try:
            if userprofile.id == null:          
                abort(403)
        except AttributeError: 
            abort(403)

        return f(*args, **kwargs)
    return decorator_function

@app.route('/')
@app.route('/home')
async def index():
    context = ""
    title = ""
    randomcard = "" 
    try:
        randomcard= await OnlineTaro.cardday()
        context = await OnlineTaro.getrandomcard()
        title = "Главная страница "
        if 'reg' in ses: 
            curstobuy=ses['reg']
        else: 
            curstobuy=0
        return render_template('start.html',randomcard=randomcard, header=header, title = title, share_url=request.base_url,curstobuy=curstobuy)
    except:
        abort(404)

@app.route('/curses/')
@app.route('/curses')
async def curses_head():
    try:
        title = "Список доступных курсов"
        randomcard= await OnlineTaro.cardday()
        context = await OnlineTaro.getrandomcard()
        curses = session.query(Curses).all()
        for curs in curses:
            curs.description = Markup(curs.description)
        if 'reg' in ses: 
            curstobuy=ses['reg']
        else: 
            curstobuy=0
        return render_template('curseshead.html',randomcard=randomcard, header=header, title = title, share_url=request.base_url, curses = curses,curstobuy=curstobuy)
    except: 
        abort(404)


@app.route('/basket')
async def basket():
    if 'reg' in ses: 
            curstobuy=ses['reg']
        else: 
            curstobuy=0
    ses['discont'] = '10%'
    title = "Корзина "
    curs = registration.getcurse()
    registration.getcast()
    randomcard= await OnlineTaro.cardday()
    return render_template('basket.html',randomcard=randomcard, header=header, title = title, share_url=request.base_url, curs = curs, cost = ses['cost'], discount = ses['discont'], cost_final = ses['total_cost'], curstobuy=curstobuy)   
    

@app.route('/reset')
async def reset():
    try:
        randomcard=await OnlineTaro.cardday()
        title = "Сброс пароля"
        return render_template('reset.html', header = header,randomcard=randomcard, title = title)
    except: 
        abort(404)


@app.route('/curses/<int:curs_id>/')
@app.route('/curses/<int:curs_id>/')
async def curse_alone(curs_id):
    try:
        randomcard=await OnlineTaro.cardday()
        curse = session.query(Curses).filter(Curses.curses_id == str(curs_id)).first()
        curse.description = Markup(curse.description)
        title = curse.name +" "
        return render_template('cursehead.html',randomcard=randomcard, header=header, title = title, share_url=request.base_url, curse = curse)    
    except AttributeError: 
        abort(404)

@app.route('/curses/subscribe/<int:curs_id>/')
@app.route('/curses/subscribe/<int:curs_id>')
def subscribe_curs(curs_id):
    try:
        for i in ses['reg']:
            if (int(i) == int(curs_id)):
                ses['find'] = 1
                break
            else: 
                ses['find'] = 0

        if ses['find'] == 0:
            ses['reg'].append(curs_id) 
 
    except: 
        ses['reg'] = []
        app.logger.info('except')
        ses['reg'].append(curs_id) 

    app.logger.info(ses['reg'])
    return redirect(url_for('curses_head'))

    
@app.route('/backoffice/userlist/<string:user_id>',methods=['POST','GET'])
@authorization_verification
def userlist_user(user_id):
    try:
        if request.method == "POST":
            logger_info.logger(request.method,request.base_url, userprofile.first_name)
        else:
            logger_info.logger(request.method,request.base_url, userprofile.first_name)
        return render_template('userlist.html',data = users_list, header=header, rule=userprofile.rule)
    except: 
        abort(404)

@app.route('/backoffice/userlist')
@authorization_verification
def userlist():
    try:
        title ="Список пользователь"
        logger_info.logger(request.method,request.base_url, userprofile.first_name)
        users_list = session.query(Users).order_by(Users.id.desc()).all()
        return render_template('userlist.html',data = users_list, header=header, title = title, rule=userprofile.rule)
    except: 
        abort(404)


@app.route('/backoffice/userlogs')
@app.route('/backoffice/userlogs?page=<int:page_num>')
@authorization_verification
def userlogs():
    try: 
        logger_info.logger(request.method,request.base_url, userprofile.first_name)
        return render_template('userlogs.html', header=header, rule=userprofile.rule)
    except: 
        abort(404)

@app.route('/backoffice/')
@app.route('/backoffice')
@authorization_verification
def backoffice():
    try: 
        logger_info.logger(request.method,request.base_url,userprofile.email) 
        return render_template('layout_lk.html', header=header, rule=userprofile.rule)    
    except: 
        abort(404)


@app.route('/backoffice/curses/')
@app.route('/backoffice/curses')
@authorization_verification
def curses():
        error_curs = 0 
        if (userprofile.cursdelerrorcount == 0): 
            error_curs = userprofile.cursdelerror
            userprofile.cursdelerrorcount +=1
       
        title="Список курсов"
        try: 
            logger_info.logger(request.method,request.base_url, userprofile.first_name)
            context = session.query(Curses).all()
        except: 
            session.rollback()

        return render_template('curses.html', context = context, header=header, title =title, errorcurs = error_curs)

@app.route('/backoffice/curses/<int:curses_id>/del=<string:delit>', methods=['GET', 'POST'])
@authorization_verification
def cursesdel(curses_id,delit):
    try:
         if request.method == "POST":
            if (delit == "true"):
                 with engine.connect() as conn:
                    transaction = conn.begin()
                    try:
                        session.query(Curses).filter(Curses.curses_id == curses_id).delete()
                        session.commit()
                        transaction.commit()
                        logger_info.logger(request.method,request.base_url, userprofile.email, "transaction.commit()")
                        userprofile.cursdelerror = 0

                    except Exception:
                        try: 
                            transaction.rollback()
                            session.rollback()
                            userprofile.cursdelerror = curses_id
                            userprofile.cursdelerrorcount = 0
                            logger_info.logger(request.method,request.base_url, userprofile.email, "Fail")
                        except: 
                            return redirect(url_for('curses'))

            return redirect(url_for('curses'))
    except:
        return abort(404)



@app.route('/backoffice/curses/addlesson/curs=<string:curses_id>', methods=['GET', 'POST'])
@app.route('/backoffice/curses/addlesson/curs=<string:curses_id>/', methods=['GET', 'POST'])
@authorization_verification
def lessonadd(curses_id):
    try: 
        count_lesson = session.query(func.count(Lessons.lesson)).filter(Lessons.curse == curses_id).scalar()
        count_lesson = count_lesson + 1
        app.logger.info(count_lesson)

        if request.method == "POST":
            curse = request.form['curse']
            lesson  = request.form['lesson']    
            name = request.form['name']  
            description = request.form['description'] 
            data = request.form['data']
            author = request.form['homework']

            with engine.connect() as conn:
                    transaction = conn.begin()
                    try:
                        session.add(Lessons(curse= curse, lesson = lesson, name=name,description=description, data = data, homework = homework))
                        transaction.commit()
                        logger_info.logger(request.method,request.base_url, userprofile.email, "transaction.commit()")
                        
                    except Exception as E:
                        transaction.rollback()
                        logger_info.logger(request.method,request.base_url, userprofile.email, E)
        else:
            return render_template('lessonnew.html', curses_id = curses_id, count_lesson = count_lesson) 
    except:
        abort(404)

       
@app.route('/backoffice/addcurse/', methods=['GET', 'POST'])
@app.route('/backoffice/addcurse', methods=['GET', 'POST'])
@authorization_verification
def addcurse():
    try: 
        title = "Создать новый курс"
        if request.method == "POST":
            name = request.form['name']
            url = request.form['url']
            author = userprofile.email
            picture = request.form['picture']
            description = request.form['description']
            try:
                cost = int(request.form['cost'])
            except:
                cost = 0

            with engine.connect() as conn:
                    transaction = conn.begin()
                    try:
                        session.add(Curses(name=name, url= url,author=author,picture=picture,description=description, cost = cost))
                        session.commit()
                        transaction.commit()
                        logger_info.logger(request.method,request.base_url, userprofile.email, "transaction.commit()")

                    except Exception as E:
                        transaction.rollback()
                        logger_info.logger(request.method,request.base_url, userprofile.email, E)

            return redirect(url_for('curses'))
        else:
            logger_info.logger(request.method,request.base_url, userprofile.email)
            return render_template('addcurse.html', user = userprofile.email, title = title,  header=header)
    except: 
        return abort(404)

@app.route('/backoffice/curses/<int:curses_id>', methods=['GET', 'POST'])
@app.route('/backoffice/curses/<int:curses_id>', methods=['GET', 'POST'])
@authorization_verification
def lessons(curses_id):
    try:
        title = "Курс " + str(curses_id)
        logger_info.logger(request.method,request.base_url, userprofile.email)
        lessons = session.query(Lessons.curse,Lessons.name,Lessons.description,Lessons.lesson,Lessons.created_on).filter(Lessons.curse == curses_id).all()
        return render_template('lessons.html', lessons = lessons, curse = curses_id, title = title, header=header)
    except:
        abort(404)
       

@app.route('/backoffice/curses/<int:curses_id>/<int:lesson_id>/del=<string:delit>', methods=['GET', 'POST'])
@authorization_verification
def lessondel(curses_id,lesson_id,delit):
    try: 
        if request.method == "POST":
            if (delit == "true"):
                with engine.connect() as conn:
                    transaction = conn.begin()
                    try:
                        session.query(Lessons).filter(and_(Lessons.curse == curses_id,Lessons.lesson == lesson_id)).delete()
                        session.commit()
                        transaction.commit()
                        logger_info.logger(request.method,request.base_url, userprofile.email, "transaction.commit()")
                    except Exception as E:
                        transaction.rollback()   
                        logger_info.logger(request.method,request.base_url, userprofile.email, E)
        return redirect(f"/backoffice/curses/{curses_id}")        
    finally:
        abort(404)
       


@app.route('/backoffice/curses/edit=<int:curse_id>', methods=['GET', 'POST'])
@authorization_verification      
def cursedit(curse_id):
    try: 
        if request.method =='POST':
            curses_id = request.form['curses_id']
            with engine.connect() as conn:
                    transaction = conn.begin()
                    try:
                        x = session.query(Curses).filter(Curses.curses_id == curses_id).first()
                        x.name =request.form['name']
                        x.url = request.form['url']
                        x.author = request.form['author']
                        x.picture = request.form['picture']
                        x.description = request.form['description']
                        x.cost = request.form['cost']
                        session.commit()
                        transaction.commit()
                        logger_info.logger(request.method,request.base_url, userprofile.email, "transaction.commit()")

                    except Exception as E:
                        transaction.rollback()   
                        logger_info.logger(request.method,request.base_url, userprofile.email, E)

            return redirect(f"/backoffice/curses/edit={curse_id}")
        else: 
            logger_info.logger(request.method,request.base_url, userprofile.first_name)
            context = session.query(Curses).filter(Curses.curses_id == curse_id).first()
            data =  context.description
            return render_template('curseedit.html', context = context, user = userprofile.email, data = data, title = "Курс" + str(curse_id), header = header)
    except: 
        abort(404)

@app.route('/backoffice/curses/edit/curs=<int:curses_id>&lesson=<int:lesson_id>/', methods=['GET', 'POST'])
@app.route('/backoffice/curses/edit/curs=<int:curses_id>&lesson=<int:lesson_id>', methods=['GET', 'POST'])
@authorization_verification
def lessonedit(curses_id,lesson_id):
    lesson = ""
    data =""
    homework = ""
    try:
        if (int(lesson_id) > 0):
            if request.method == 'GET':
                lesson = session.query(Lessons).filter((Lessons.curse == curses_id) & (Lessons.lesson == lesson_id)).first()
                data = lesson.data
                homework = lesson.homework
                logger_info.logger(request.method,request.base_url, userprofile.email)
                return render_template('lessonedit.html', lesson = lesson, data = data, homework = homework)

            if request.method == 'POST':
                with engine.connect() as conn:
                    transaction = conn.begin()
                    lesson = request.form['lesson']
                    curse = request.form['curse']

                    try:
                        x = session.query(Lessons).filter((Lessons.curse == curses_id) & (Lessons.lesson == lesson_id)).first()
                        x.homework =request.form['homework']
                        x.description = request.form['description']
                        x.data =request.form['data']
                        x.name = request.form['name']
                        x.lesson = lesson 
                        session.commit()
                        transaction.commit()
                        logger_info.logger(request.method,request.base_url, userprofile.email, "transaction.commit()")
                    except Exception as E:
                        transaction.rollback()
                        logger_info.logger(request.method,request.base_url, userprofile.email, E)

                lesson = session.query(Lessons).filter((Lessons.curse == curses_id) & (Lessons.lesson == lesson_id)).first()
                data = lesson.data
                homework = lesson.homework
                return render_template('lessonedit.html', lesson = lesson, data = data, homework = homework)
       
        if (int(lesson_id) == 0):
            if request.method == 'POST':
                curse = request.form['curse']
                lesson = request.form['lesson']
                name = request.form['name']
                description = request.form['description']
                data = request.form['data']
                homework = request.form['homework']
                with engine.connect() as conn:
                    transaction = conn.begin()
                    try:
                        session.add(Lessons(curse=curse, name= name,description=description,lesson=lesson,homework=homework,data=data))
                        session.commit()
                        transaction.commit() 
                        logger_info.logger(request.method,request.base_url, userprofile.email, "transaction.commit()")
                    except Exception as E:
                        transaction.rollback()
                        logger_info.logger(request.method,request.base_url, userprofile.email, E)
                    
                lesson = session.query(Lessons).filter((Lessons.curse == curse) & (Lessons.lesson == lesson)).first()
                data = lesson.data
                homework = lesson.homework
                return render_template('lessonedit.html', lesson = lesson, data=data, homework = homework)      
    except:
        abort(404)


@app.route('/backoffice/curses/view/curs=<int:curses_id>&lesson=<int:lesson_id>', methods=['GET', 'POST'])
@authorization_verification
def lessonview(curses_id,lesson_id):
    try: 
        title = "Урок " + str(lesson_id) + " Курс" + str(curses_id)
        logger_info.logger(request.method,request.base_url, userprofile.first_name)
        lessondata = session.query(Lessons).filter(and_(Lessons.curse  == curses_id, Lessons.lesson == lesson_id)).first()
        data = Markup(lessondata.data)
        homework = Markup(lessondata.homework)
        return render_template('lesson.html', data =data, homework = homework, title = title, header=header)
    except: 
        abort(404)
        


@app.route('/backoffice/settings', methods=['GET', 'POST'])
@authorization_verification
def setting():
    try: 
        title = "Настройка сайта"
        session_data = session.query(Settings_site).filter(Settings_site.id == '1').first()
        if request.method == 'POST':
            try:
                site_name1 = request.form['name']
                site_name_eng1 = request.form['name_eng']
                email_admin1 = request.form['email']
                email_smtp1 = request.form['smtp']
                description1 = request.form['description'] 
                meta_tag1 = request.form['meta_tag']
                
                with engine.connect() as conn:
                        transaction = conn.begin()
                        try:
                            x = session.query(Settings_site).get(1)
                            x.site_name =site_name1 
                            x.site_name_eng1 =site_name_eng1
                            x.email_admin =email_admin1
                            x.email_smtp = email_smtp1
                            x.description = description1
                            x.meta_tag = meta_tag1
                            session.commit()
                            transaction.commit() 
                            logger_info.logger(request.method,request.base_url, userprofile.email, "transaction.commit()")
                        except Exception as E:
                            transaction.rollback()
                            logger_info.logger(request.method,request.base_url, userprofile.email, E)
                return redirect(url_for('setting'))
            except: 
                return render_template('setting.html', title= title, header=header)
        else: 
            logger_info.logger(request.method,request.base_url, userprofile.first_name)
            return render_template('setting.html', data = session_data, title = title, header=header)
    except: 
        abort(404)


@app.route('/backoffice/taroedit/<int:card_id>', methods=['GET', 'POST'])
@authorization_verification
def taroonlineeditcard(card_id=1):
    try:
        logger_info.logger(request.method,request.base_url, userprofile.first_name)
        if request.method == 'POST':
            id = request.form['id']
            carta = request.form['carta']
            eng = request.form['eng']
            type_carta = request.form['type_carta']
            type_carta_eng= request.form['type_carta_eng']
            graph_simphol = request.form['graph_simphol']
            name_carta = request.form['name_carta']
            name2_carta = request.form['name2_carta']
            description_cart = request.form['description_cart']
            general_carta = request.form['general_carta']
            psih_har= request.form['psih_har']
            zodiak = request.form['zodiak']
            starhie_arkan = request.form['starhie_arkan']
            mechi = request.form['mechi']
            pentakl = request.form['pentakl']
            zhezl = request.form['zhezl']
            kubki= request.form['kubki']
            busnes1 = request.form['busnes1']
            busnes2 = request.form['busnes2']
            love1 = request.form['love1']
            love2 = request.form['love2']
            yesno = request.form['yesno']

            with engine.connect() as conn:
                        transaction = conn.begin()
                        try:
                            x = session.query(Onlinetaro).filter(Onlinetaro.id == id).first()
                            x.carta =carta
                            x.eng =eng
                            x.type_carta =type_carta
                            x.type_carta_eng = type_carta_eng
                            x.graph_simphol = graph_simphol
                            x.name_carta = name_carta
                            x.name2_carta=name2_carta
                            x.description_cart=description_cart
                            x.general_carta=general_carta
                            x.psih_har= psih_har
                            x.zodiak= zodiak
                            x.starhie_arkan = starhie_arkan
                            x.mechi=mechi
                            x.pentakl=pentakl
                            x.kubki=kubki
                            x.zhezl=zhezl
                            x.busnes1=busnes1
                            x.busnes2=busnes2
                            x.love1=love1
                            x.love2=love2
                            x.yesno=yesno
                            session.commit()
                            transaction.commit() 
                            logger_info.logger(request.method,request.base_url, userprofile.email, "transaction.commit()")
                        except Exception as E:
                            transaction.rollback()
                            logger_info.logger(request.method,request.base_url, userprofile.email, E)

            return redirect("/backoffice/taroedit/{card_id}")
           
        else: 
            context = session.query(Onlinetaro).all() 
            context2 = session.query(Onlinetaro).filter(Onlinetaro.id == int(card_id)).first() 
            return render_template('taroonlineedit.html', data = context, data2=context2, title= "Редактирование Таро карт", header=header)
    except: 
        abort(404)

 
       
@app.route('/backoffice/taroedit', methods=['GET', 'POST'])
@authorization_verification
def taroonlineedit():
    try: 
        context = session.query(Onlinetaro).all() 
        return render_template('taroonlineedit.html', data = context, title= "Редактирование Таро карт", header=header)
    except: 
        abort(404)

@app.route('/login')
async def login_user():
    try: 
        title = "Регистрация "
        randomcard=await OnlineTaro.cardday()

        url = render_template('/auth/login.html', header=header, title = title, share_url=request.base_url, randomcard = randomcard )
        try:
                 if userprofile.id != None and ses['log_in'] == True:      
                    return redirect(url_for('backoffice'))
                 else:
                    try:
                        if ses['logged_failed'] == True:
                            return render_template('/auth/login.html',error = "Ошибка в логине или пароле", header=header, title= title, share_url=request.base_url, randomcard = randomcard)        
                    except: 
                        ses['logged_failed'] = False 
                        return url
        except:  
            return url
    except:
        abort(404)  

    
@app.route('/auth/login', methods=['POST', 'GET'])
async def login_auth():
    try:
        if request.method == 'POST':
            user_email = request.form['email'].strip()
            user_password =  request.form['password']
            user = session.query(Users).filter(Users.email == user_email).first()
            message_bytes = user_password.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')
            if user!=None and user.password == base64_message:
                ses['user'] =  user_email
                global userprofile
                if (int(user.rule) == 1):
                    userprofile = SuperUser()
                else: 
                    userprofile = User()

                userprofile.id = user.id
                userprofile.first_name = user.first_name
                userprofile.last_name = user.last_name
                userprofile.surname = user.surname
                userprofile.telegram = user.telegram
                userprofile.whatsapp = user.whatsapp
                userprofile.email = user.email
                userprofile.rule = user.rule
                
                global logger_info
                logger_info = Logger_info()
                ses['log_in'] = True
                logger_info.logger(request.method,request.base_url, userprofile.email)
                return redirect(url_for('backoffice'))
                
            else:
                ses['logged_failed'] = True
                return redirect(url_for('login_user'))
        if request.method == 'GET':
            return redirect(url_for('login_user'))
    except:
        abort(404)

           
@app.route('/logout')
def logout():
    try: 
        ses.pop('logged_in', False)
        ses.pop('logged_failed', None)
        flash('You were logged out')
        global userprofile
        userprofile = ""
        return redirect(url_for('index'))
    except: 
        abort(404)


@app.route('/taro/<string:category>/', methods=['GET', 'POST'])
@app.route('/taro/<string:category>', methods=['GET', 'POST'])
async def tarocategory(category):
    try: 
        author = header['site_name']
        randomcard= await OnlineTaro.cardday()
        share_url = request.base_url
        site_name = header['site_name']

        url = "/taro/"
        if (str(category)=="mladshie-arkany"):
            title = "Карты Таро: Младшие Арканы"
            keywords = "Карты Таро: Младшие Арканы"
            context = session.query(Onlinetaro.id,Onlinetaro.type_carta_eng,Onlinetaro.type_carta,Onlinetaro.carta,Onlinetaro.eng,Onlinetaro.img,Onlinetaro.graph_simphol).filter(Onlinetaro.type_carta_eng != "starshui-arkan").all()
            description = "Младшие арканы Таро 56 карт описывают бытовые детали и ситуации. Арканы такого типа представляют собой 4 набора, разделенные по мастям и состоящие из числовых и придворных карт. Каждая масть насчитывает 14 арканов"
           
            return render_template('taro.html', data = context, category=category,url=url, randomcard=randomcard, title = title, descriptioncategory = 1,share_url=request.base_url, keywords = keywords, description = description, author = author, site_name = site_name, header=header)
        
        if (str(category)=="starshui-arkan"):
            title = "Карты Таро: Старшие Арканы"
            keywords = "Карты Таро: Старшие Арканы"
            description = "Kлaccичecкий вapиaнт гaдaния нa Tapo пpeдлaгaeт чeткoe pacпpeдeлeниe кapт нa Cтapшиe и Mлaдшиe Apкaны. Гpуппa Cтapшиx пpeдcтaвлeнa 22 кapтaми, кoтopыe и cтaнoвятcя бaзoй для пpинципa тpaктoвки в pacклaдe (ecли oни выпaдaют и иcпoльзуютcя). Oни oтвeчaют зa вpeмeннoe oпиcaниe пpoшлoгo, будущeгo и тeпepeшнeй peaльнocти, a тaкжe oтвeчaют нa выcшиe филocoфcкиe вoпpocы. Дaвaйтe внимaтeльнo paccмoтpим знaчeниe для кaждoй тaкoй кapты."
            context = session.query(Onlinetaro.id,Onlinetaro.type_carta_eng,Onlinetaro.type_carta,Onlinetaro.carta,Onlinetaro.eng,Onlinetaro.img,Onlinetaro.graph_simphol).filter(Onlinetaro.type_carta_eng == category).all()    
            return render_template('taro.html', data = context, category=category,url=url, randomcard=randomcard, title = title, descriptioncategory = 1,share_url=request.base_url, keywords = keywords, description = description, author = author, site_name = site_name, header=header)
        
        if (str(category) == "mechi" or str(category) == "pentakli" or str(category) == "zhezly" or str(category) == "kubki"):
            title = "Младшие Арканы "
            keywords = "Младшие Арканы"
            description = "Младшие арканы Таро – 56 карт – описывают бытовые детали и ситуации. Арканы такого типа представляют собой 4 набора, разделенные по мастям и состоящие из числовых и придворных карт. Каждая масть насчитывает 14 арканов"
            context = session.query(Onlinetaro.id,Onlinetaro.type_carta_eng,Onlinetaro.type_carta,Onlinetaro.carta,Onlinetaro.eng,Onlinetaro.img,Onlinetaro.graph_simphol).filter(Onlinetaro.type_carta_eng == category).all()    
            return render_template('taro.html', data = context, category=category,url=url, randomcard=randomcard, title = title, descriptioncategory = 1, share_url=request.base_url, keywords = keywords, description = description, author = author, site_name = site_name, header=header)
        
        else: 
            array= getmatch(category)
            context = session.query(Onlinetaro).filter(Onlinetaro.eng == category).first()
            if (context):
                url = "/taro/"
                context2 = session.query(Onlinetaro.img,Onlinetaro.carta,Onlinetaro.eng, Onlinetaro.type_carta_eng).all()
                title=str(context.carta)+ "— обозначение "+context.carta+" в Таро, значение в отношениях и любви, сочетание с другими картами, толкование перевернутой карты Уэйта Райдера"
                keywords=str(context.carta)
                description="Для точного и правдивого гадания на картах Таро нужно знать подробное значение этих карт. Стандартная колода состоит из 78 карт, каждая из которых имеет определенное значение как и в прямом, так и в перевернутом положении. Ниже представлен список всех Таро карт с подробным толкованием на все случаи жизни: ближайшее будущее, ситуация или вопрос, гадание на любовь и отношения, гадание на мысли, ситуацию в работе и многое другое."
                return render_template('tarocard.html', data = context, data2 = context2,url=url, randomcard=randomcard, title=title, array=array, descriptioncategory = 0, share_url=request.base_url, keywords = keywords, description = description, author = author, site_name = site_name, header=header)
            else: 
                abort(404)
    except: 
        abort(404)


def getmatch(name):
    try:
        context = session.query(Onlinetaro.starhie_arkan,Onlinetaro.mechi,Onlinetaro.pentakl,Onlinetaro.zhezl,Onlinetaro.kubki).filter(Onlinetaro.eng == name).first()
        starhie_arkan = (''.join(context[0])).split("+")
        mechi = (''.join(context[1])).split("+")
        pentakl = (''.join(context[2])).split("+")
        zhezl = (''.join(context[3])).split("+")
        kubki = (''.join(context[4])).split("+")
        array = []
        array.append(starhie_arkan)
        array.append(mechi)
        array.append(pentakl) 
        array.append(zhezl) 
        array.append(kubki)
        return array
    except: 
        abort(404)


@app.route('/taro/<string:category>/<string:name>', methods=['GET', 'POST'])
async def tarocard(category, name):
    try: 
        url = "/taro/"
        site_name = header['site_name']
        randomcard=await OnlineTaro.cardday()
        context = session.query(Onlinetaro).filter(Onlinetaro.eng == name).first()
        context2 = session.query(Onlinetaro.img,Onlinetaro.carta,Onlinetaro.eng, Onlinetaro.type_carta_eng).all()
        title=str(context.carta)+ "— обозначение "+context.carta+" в Таро, значение в отношениях и любви, сочетание с другими картами, толкование перевернутой карты Уэйта Райдера"
        array= getmatch(name)
        return render_template('tarocard.html', data = context, data2 = context2,url=url, author = site_name, keywords=context.name2_carta, randomcard=randomcard, title=title, array=array, description = context.description_cart, share_image = context.img, share_url=request.base_url, site_name= site_name, header=header)
    except:
        abort(404)    

@app.route('/taro')
async def taro():
    try:
        randomcard=await OnlineTaro.cardday()
        title = "Карты Таро: Значение и толкование"
        url="/taro/"
        context = session.query(Onlinetaro).all()
        description = "Для точного и правдивого гадания на картах Таро нужно знать подробное значение этих карт. Стандартная колода состоит из 78 карт, каждая из которых имеет определенное значение как и в прямом, так и в перевернутом положении. Ниже представлен список всех Таро карт с подробным толкованием на все случаи жизни: ближайшее будущее, ситуация или вопрос, гадание на любовь и отношения, гадание на мысли, ситуацию в работе и многое другое."
        keywords = "Карты, таро, таролог, аркан"
        return render_template('taro.html', data = context, all="1", url = url, randomcard=randomcard, description = description,descriptioncategory=0, title = title, share_url=request.base_url, keywords =keywords, header=header)
    except: 
        abort(404)    

@app.route('/backoffice/taro/')
@app.route('/backoffice/taro')
async def backofficetaro():
    try:
        randomcard=await OnlineTaro.cardday()
        title = "Карты Таро: Значение и толкование"
        url="/backoffice/taro/"
        context = session.query(Onlinetaro).all()
        return render_template('backoffice_taro.html', data = context, all="1", url = url, randomcard=randomcard, title = title)
    except:
        abort(404)


@app.route('/backoffice/taro/<string:category>/', methods=['GET', 'POST'])
@app.route('/backoffice/taro/<string:category>', methods=['GET', 'POST'])
async def backoffitarocategory(category):
    try:
        randomcard= await OnlineTaro.cardday()
        title = ""
        url="/backoffice/taro/"
        if (str(category)=="mladshie-arkany"):
            title = "Карты Таро: Младшие Арканы"
            context = session.query(Onlinetaro.id,Onlinetaro.type_carta_eng,Onlinetaro.type_carta,Onlinetaro.carta,Onlinetaro.eng,Onlinetaro.img,Onlinetaro.graph_simphol).filter(Onlinetaro.type_carta_eng != "starshui-arkan").all()
            return render_template('backoffice_taro.html', data = context, category=category,url=url, randomcard=randomcard, descriptioncategory = 1, title = title, title2=title)
        if (str(category)=="starshui-arkan"):
            title = "Карты Таро: Старшие Арканы"
            context = session.query(Onlinetaro.id,Onlinetaro.type_carta_eng,Onlinetaro.type_carta,Onlinetaro.carta,Onlinetaro.eng,Onlinetaro.img,Onlinetaro.graph_simphol).filter(Onlinetaro.type_carta_eng == category).all()    
            return render_template('backoffice_taro.html', data = context, category=category,url=url, randomcard=randomcard, descriptioncategory = 1, title = title, title2=title)
        if (str(category) == "mechi" or str(category) == "pentakli" or str(category) == "zhezly" or str(category) == "kubki"):
            title = "Младшие Арканы "
            context = session.query(Onlinetaro.id,Onlinetaro.type_carta_eng,Onlinetaro.type_carta,Onlinetaro.carta,Onlinetaro.eng,Onlinetaro.img,Onlinetaro.graph_simphol).filter(Onlinetaro.type_carta_eng == category).all()    
            return render_template('backoffice_taro.html', data = context, category=category,url=url, randomcard=randomcard, descriptioncategory = 1, title = title, title2=title)
        else: 
            array= getmatch(category)
            context = session.query(Onlinetaro).filter(Onlinetaro.eng == category).first()
            if (context):
                url = "/taro/"
                context2 = session.query(Onlinetaro.img,Onlinetaro.carta,Onlinetaro.eng, Onlinetaro.type_carta_eng).all()
                title=str(context.carta)+ "— обозначение "+context.carta+" в Таро, значение в отношениях и любви, сочетание с другими картами, толкование перевернутой карты Уэйта Райдера"
                return render_template('backoffice_taro.html', data = context, data2 = context2,url=url, randomcard=randomcard, title=title, array=array)
            else: 
                abort(404)
    except:
        abort(404)

@app.route('/backoffice/taro/<string:category>/<string:name>', methods=['GET', 'POST'])
def backoffitarotarocard(category, name):
    try:
        url = "/backoffice/taro/"
        context = session.query(Onlinetaro).filter(Onlinetaro.eng == name).first()
        title=str(context.carta)+ "— обозначение "+context.carta+" в Таро, значение в отношениях и любви, сочетание с другими картами, толкование перевернутой карты Уэйта Райдера"
        array= getmatch(name)
        context2 = session.query(Onlinetaro.img,Onlinetaro.carta,Onlinetaro.eng, Onlinetaro.type_carta_eng).all()
        return render_template('backtarocard.html', data = context, data2=context2, url=url, title=title, array=array, curs = "1", title2=context.name_carta)
    except:
        abort(404)


@app.route('/taroonline/')
@app.route('/taroonline')
async def taroonline():
    try:
        randomcard=await OnlineTaro.cardday()
        return render_template('taroonline.html', randomcard=randomcard, header=header)
    except:
        abort(404)

@app.route('/taroonline/vokzal/', methods=['GET', 'POST'])
@app.route('/taroonline/vokzal', methods=['GET', 'POST'])
async def vokzal():
    try: 
        randomcard= await OnlineTaro.cardday()
        if (request.method == 'POST'):
            item = 17
            generated_card = await OnlineTaro.generated_card_func(item)
            context  = await OnlineTaro.generated_card_info(item, generated_card)
            return render_template('vokzal.html', context = context,data=1, randomcard=randomcard, header=header)
        else:
            return render_template('vokzal.html', data = 0, randomcard=randomcard, rubashka=rubashka, header=header)
    except: 
        abort(404)

@app.route('/taroonline/relation/', methods=['GET', 'POST'])
@app.route('/taroonline/relation', methods=['GET', 'POST'])
async def relation():
    try:
        randomcard= await OnlineTaro.cardday()
        if request.method == 'POST':
            item = 8
            generated_card = await OnlineTaro.generated_card_func(item)
            context  = await OnlineTaro.generated_card_info(item, generated_card)
            return render_template('relation.html', context = context, data=1, randomcard=randomcard, header=header)
        else:
            return render_template('relation.html', data = 0, randomcard=randomcard, rubashka = rubashka, header=header)
    except: 
        abort(404)

@app.route('/taroonline/yesno/', methods=['GET', 'POST'])
@app.route('/taroonline/yesno', methods=['GET', 'POST'])
async def yesno():
    try: 
        randomcard=await OnlineTaro.cardday()
        if request.method == 'POST':
            item = 3
            generated_card = await OnlineTaro.generated_card_func(item)
            rotate = await OnlineTaro.generated_card_position()
            context  = await OnlineTaro.generated_card_info(item, generated_card)
            return render_template('yesno.html', context = context, rotate=rotate, data=1, randomcard=randomcard, header=header)
        else:
            return render_template('yesno.html',data=0, randomcard=randomcard, rubashka = rubashka, header=header)
    except:
        abort(404)

@app.route('/taroonline/keltkrest/', methods=['GET', 'POST'])        
@app.route('/taroonline/keltkrest', methods=['GET', 'POST'])
async def keltkrest():
    try: 
        randomcard=await OnlineTaro.cardday()
        if request.method == 'POST':
            item = 10
            generated_card = await OnlineTaro.generated_card_func(item)
            rotate = await OnlineTaro.generated_card_position()
            context  =await OnlineTaro.generated_card_info(item, generated_card)
            return render_template('keltkrest.html', context = context, data = 1, randomcard=randomcard, header=header)
        else:
            return render_template('keltkrest.html', data = 0, randomcard=randomcard, rubashka = rubashka, header=header)
    except: 
        abort(404)

@app.route('/taroonline/face/', methods=['GET', 'POST'])
@app.route('/taroonline/face', methods=['GET', 'POST'])
async def face():
    try:
        randomcard= await OnlineTaro.cardday()
        if request.method == 'POST':
            item = 8
            generated_card = await OnlineTaro.generated_card_func(item)
            rotate = await OnlineTaro.generated_card_position()
            context  = await OnlineTaro.generated_card_info(item, generated_card)
            return render_template('face.html', context = context, data = 1, randomcard=randomcard, header=header)
        else:
            return render_template('face.html', data = 0, randomcard=randomcard, rubashka = rubashka, header=header)
    except: 
        abort(404)

@app.route('/taroonline/choice/', methods=['GET', 'POST'])
@app.route('/taroonline/choice', methods=['GET', 'POST'])
async def choice():
    try:
        randomcard=await OnlineTaro.cardday()
        if request.method == 'POST':
            item = 7
            generated_card = await OnlineTaro.generated_card_func(item)
            rotate = await OnlineTaro.generated_card_position()
            context  = await OnlineTaro.generated_card_info(item, generated_card)
            return render_template('choice.html', context = context, data = 1, randomcard=randomcard, header=header)
        else:
            return render_template('choice.html', data = 0, randomcard=randomcard, rubashka = rubashka, header=header)
    except: 
        abort(404)

@app.route('/taroonline/lover/', methods=['GET', 'POST'])
@app.route('/taroonline/lover', methods=['GET', 'POST'])
async def lover():
    try:
        randomcard= await OnlineTaro.cardday()
        if request.method == 'POST':
            item = 6
            generated_card =await OnlineTaro.generated_card_func(item)
            rotate = await OnlineTaro.generated_card_position()
            context  = await OnlineTaro.generated_card_info(item, generated_card)
            return render_template('lover.html', context = context, data = 1, randomcard=randomcard, header=header)
        else:
            return render_template('lover.html', data = 0, randomcard=randomcard, rubashka = rubashka, header=header)
    except: 
        abort(404);

@app.route('/taroonline/man/', methods=['GET', 'POST'])
@app.route('/taroonline/man', methods=['GET', 'POST'])
async def man():
    try: 
        randomcard=await OnlineTaro.cardday()
        if request.method == 'POST':
            item = 7
            generated_card =await OnlineTaro.generated_card_func(item)
            rotate = await OnlineTaro.generated_card_position()
            context  = await OnlineTaro.generated_card_info(item, generated_card)
            return render_template('man.html', context = context, data = 1, randomcard=randomcard, header=header)
        else:
            return render_template('man.html', data = 0, randomcard=randomcard, rubashka = rubashka, header=header)
    except: 
        abort(404)

@app.route('/pifagor')
async def pifagor():
    try:
        randomcard= await OnlineTaro.cardday()
        return render_template('pifagor.html', randomcard=randomcard, header=header)
    except:
        abort(404)

def getsiteparam(item="all"):
    settings = ""
    try:
        if (item=="all"):
            settings = session.query(Settings_site).get(1)
            return settings
    except: 
        abort(404)

@app.errorhandler(404)
async def page_not_found(e):
    randomcard=""
    context =""
    try: 
        randomcard = await OnlineTaro.cardday()
        context = await OnlineTaro.getrandomcard()
        return render_template('404.html',card = context, randomcard=randomcard, header = header), 404
    except: 
        abort(404)

@app.errorhandler(403)
async def forbidden(e):
    randomcard=""
    context = ""
    try: 
        randomcard =await OnlineTaro.cardday()
        context = await OnlineTaro.getrandomcard()
        return render_template('403.html',card = context, randomcard=randomcard, header = header), 403
    except:
        abort(404)

@app.errorhandler(500)    
async def internal_server_error(e):
    randomcard = ""
    context = ""
    try: 
        randomcard=await OnlineTaro.cardday()
        context =await OnlineTaro.getrandomcard()
        return render_template('404.html',card = context, randomcard=randomcard, header = header), 500
    except:
        abort(404)


class Api():
    checkuser = False 

    def currentusercheck (self, user):
        pass

    def getcard(self,card):
        session = Session(bind=engine)
        data = []
        
        try: 
             if (int(card) and int(card) < 78):
                context = session.query(Onlinetaro).filter(Onlinetaro.id == int(card)).first()
                card_data = {
                'id': context.id,
                'carta': context.carta,
                'eng': context.eng,
                'type_carta': context.type_carta,
                'img': context.img,
                'graph_simphol': context.graph_simphol,
                'name': context.name_carta,
                'name2_carta': context.name2_carta,
                'description_cart': context.description_cart,
                'psih_har': context.psih_har,
                'zodiak': context.zodiak,
                'match':
                {'starhie_arkan':context.starhie_arkan,
                'mechi':context.mechi,
                'pentakl':context.pentakl,
                'zhezl':context.zhezl,
                'kubki':context.kubki},
                'business':
                {'plus':context.busnes1,
                'minus':context.busnes2,},
                'love':
                {'plus':context.love1,
                'minus':context.love2,},
                'yesno':context.yesno},
                data.append(card_data)

        except ValueError:
            if (str(card)=="all"):
                context = session.query(Onlinetaro).all()
                for i in range(78):
                    card_data = {
                    'id': context[i].id,
                    'carta': context[i].carta,
                    'eng': context[i].eng,
                    'type_carta': context[i].type_carta,
                    'img': context[i].img,
                    'graph_simphol': context[i].graph_simphol,
                    'name': context[i].name_carta,
                    'name2_carta': context[i].name2_carta,
                    'description_cart': context[i].description_cart,
                    'psih_har': context[i].psih_har,
                    'zodiak': context[i].zodiak,
                     'match':
                {'starhie_arkan':context[i].starhie_arkan,
                'mechi':context[i].mechi,
                'pentakl':context[i].pentakl,
                'zhezl':context[i].zhezl,
                'kubki':context[i].kubki},
                    'business':
                    {'plus':context[i].busnes1,
                    'minus':context[i].busnes2,},
                    'love':
                    {'plus':context[i].love1,
                    'minus':context[i].love2,},
                    'yesno':context[i].yesno}
                    data.append(card_data)
            else:
                abort(404)

        return data

@app.route('/api/get/<string:card>', methods=['GET'])
def get_card(card):
    ''''api = Api()'''
    '''data = api.getcard(card) '''
    '''Logger.logger(request.method,request.base_url, "323423434324")'''
    '''return jsonify({'card':data})'''
    pass

if __name__ == "__main__":
    '''create_db()'''
    from waitress import serve    
    Settings.getglobalsettings()
    registration = Registration()
    app.config['SECRET_KEY'] = '56756756756757wqwreewdewfderffdrwerwffretewe43ewt'    
    app.run(host='0.0.0.0',port=80,debug=True)
    
    '''serve(app,host='0.0.0.0',port=80)'''
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(500, internal_server_error)
