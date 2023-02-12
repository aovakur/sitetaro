from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from flask import Flask
from FlaskWebProject2 import app


"""
class mail():
  def SentMessage(mail):
    try: 
      msg = MIMEMultipart()
      message = "Вы зарегистрировались на сайте СДЮШ Павловского Посада"
      password = "okgqmfflukipscgi"
      msg['From'] = "andrey@businessarchitecture.ru"
      msg['To'] = mail
      msg['Subject'] = "Регистрация на сайте детской школы"
      app.logger.info('Отправляется письмо')
      msg.attach(MIMEText(message, 'plain'))
      server = smtplib.SMTP_SSL('smtp.yandex.ru',465)
      server.login(msg['From'], password)
      server.sendmail(msg['From'], msg['To'], msg.as_string())
      server.quit()
      app.logger.info('Письмо отправлено')
      message = True
    except: 
      app.logger.info('Ошибка')
      message = False
    finally: 
      return bool(message)
"""
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/auth/login.html', error = "У вас нет доступа, авторизуйтесь", title="Список пользователей")
 
"""
@app.route('/lk')
def authority():
    alllogging = logging.query.order_by(logging.id.desc()).limit(3).all()
    try:
       if session['logged_in'] == True:
         return render_template('charts.html', title="Мониторинг заявок",alllog = alllogging)   
       else: 
         return render_template('login.html', error = "У вас нет доступа, авторизуйтесь",alllog = alllogging)
    except:
        return render_template('login.html', error = "У вас нет доступа, авторизуйтесь",alllog = alllogging)

@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')


@app.route('/newaplication', methods=['GET', 'POST'])
def newaplication():

    if request.method == 'POST':    
      try: 
        ins3 = application12.insert().values(
        name = request.form['name'],
        familia = request.form['familia'],
        otchestvo = request.form['otchestvo'],
        mob=request.form['mob'],
        address = request.form['address'])
        conn.execute(ins3)
        Session1.commit()
        data = request.form['familia'] + " " + request.form['name'] + " "+request.form['otchestvo']
        logger("Новая заявка успешно добавлена", data)
        return render_template('newapplication.html', application_new = "Заявка добавлена", title ="Новая заявка")
      except: 
        data = request.form['familia'] + " " + request.form['name'] + " "+request.form['otchestvo']
        logger("Новая заявка не добавлена", data)
        return render_template('newapplication.html', application_new = "Заявка не добавлена, повторите попытку", title ="Новая заявка")


    else: 
      return render_template('newapplication.html', title ="Новая заявка")


@app.route('/application?page=<int:page_num>', methods=['GET', 'POST'])
@app.route('/application', methods=['GET', 'POST'])
def application(page_num=1):

    lastrow = Session1.query(Application1).order_by(Application1.id.desc()).first()
    firstrow = int(lastrow.id)-500
    allapplication =  Application1.query.order_by(Application1.id.desc()).filter(Application1.id>firstrow).paginate(per_page=20, page=page_num, error_out=True)
    acts = Acts.query.order_by(Acts.id)
    if request.method == 'POST':
      return render_template('application.html', data = allapplication, title ="Список заявок c актами", acts = acts)
    else: 
      return render_template('application.html', data = allapplication, title ="Список заявок с актами", acts = acts)

@app.route('/allact')
def allact():
  
    ins1 = Acts.insert().values(
            id_name = 1,
            file = "1",
            sum = "324",)
    conn.execute(ins1)
    Session1.commit()

    acts2 = Session1.query(Acts)
    return render_template('tables.html', acts = acts2)

def allowed_file(filename):
    """"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uslugi', methods=['GET', 'POST'])
def uslugi():
  alluslugi = Session1.query(uslugi1)
  if request.method == 'POST':
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
    full_path = os.path.join(app.config['UPLOAD_FOLDER'])
    full_path= full_path +"/"+ f.filename
    data = pd.read_excel(full_path,engine='openpyxl',index_col=None, header=None)
    Session1.query(uslugi1).delete()
    Session1.commit() 
    try:  
     
      for col_name, row in data.iterrows():
         if  row[0] > 0:
            ins1 = uslugi1.insert().values(
            id = int(row[0]),
            name = row[1],
            unit = row[2],
            cast =  int(row[3]),)
            app.logger.info(row[0])
            conn.execute(ins1)
            Session1.commit()
         else:
            break 

      logger("Список услуг обновлен", f.filename )      
      return render_template('uslugi.html', data = alluslugi, title = "Список услуг", name = f"Файл {f.filename} успешно загружен")
        
    except ValueError:
      app.logger.info("Ошибка в ", f.filename)
      return render_template('uslugi.html', data = alluslugi, title = "Список услуг", name = f"Файл {f.filename} успешно не загружен, повторите обновление")

  else: 
    return render_template('uslugi.html', data = alluslugi, title = "Список услуг")


@app.route('/register', methods=['GET', 'POST'])
def register():
  
  if request.method == 'POST':

    customer_name = request.form['name']
    customer_familia =  request.form['familia']
    customer_otchestvo = request.form['otchestvo']
    customer_mob = request.form['mob']
    customer_mail = request.form['email']
    customer_password = request.form['password']
    customer_passwordrepeat = request.form['passwordrepeat']

    try:
      if customer_passwordrepeat==customer_password and (len(customer_password) > 6):
        ins = userorg.insert().values(
        name =  customer_name,
        familia = customer_familia,
        otchestvo = customer_otchestvo,
        mob= customer_mob,
        mail = customer_mail,
        password = base64.b64encode(customer_password.encode('ascii')),
        check_rule = 1,
        rule = 5,
        block = 0)
        conn.execute(ins)
        data = customer_familia + " "+customer_name +" " +  customer_otchestvo
        logger("Успешная регистрация", data)
        return render_template('reg.html',error = "Успешная регистрация") 
      else:
        return render_template('reg.html', error = "Ошибка в регистрации, повторите попытку", title = "Регистрация")

    except:
        data = customer_familia + customer_name +  customer_otchestvo
        logger("Ошибка в регистрации, повторите попытку", data)
        return render_template('reg.html', error = "Ошибка в регистрации, повторите попытку", title = "Регистрация")

    
  else: 
      return render_template('reg.html', title = "Регистрация")


@app.route('/auth/logout')
def logout():
  session.pop('logged_in', None)
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('home'))

@app.route('/userlist')
def userlist():
  if session['logged_in'] == True: 
    
    alluser = Session1.query(userorg).order_by(userorg.c.id.desc())
    return render_template('userlist.html', data = alluser, title="Список пользователей")
  else: 
    return render_template('/auth/login.html', error = "У вас нет доступа, авторизуйтесь", title="Список пользователей")

@app.route('/userlist?approve=<int:id>', methods=['GET'])
def userapprove():
    return render_template('userlist.html')

@app.route('/userlist?edit=<int:id>', methods=['GET'])
def useredit():
    return render_template('userlist.html')

@app.route('/userlist?block=<int:id>', methods=['GET'])
def userblock():
    return render_template('userlist.html')

@app.route('/act', methods=['GET'])
@app.route('/act?id=<int:id>&act=<int:idact>', methods=['GET'])
def act():
    return render_template('newact.html')    

@app.route('/createact', methods=['GET', 'POST'])
@app.route('/createact?id=<int:id>&room=<int:roomcount>', methods=['GET', 'POST'])
def createact():
  client = request.args.get('id')
  if request.method == 'POST':
   count_uslug=100
   user = {
   "id": "application1",
   "name":"Name",
   "address": "address"}
   app.logger.info(user)

   for i in range (1,count_uslug): 
    try:
      if (len(request.form[f'row{6}_{i}'])>0 and request.form[f'row{6}_{i}'] == "on" ):
          data = {
            f"usluga={i}": {
            "name": request.form[f'row{1}_{i}'],
            "volume":request.form[f'row{4}_{i}'],
            "sum": request.form[f'row{5}_{i}'],
            "extra": "0"
            }}
          app.logger.info(data)
      else: 
        pass
    except:
      pass

   for i in range (1,50): 
      try:
        if (request.form[f'extra{6}_{i}'] == "on"):
            data = {
              f"usluga={count_uslug}": {
              "name": request.form[f'extra{1}_{i}'],
              "volume":request.form[f'extra{4}_{i}'],
              "sum": request.form[f'extra{5}_{i}'],
              "extra": "1"
              }}
            count_uslug=count_uslug+1
            app.logger.info(data)
        else: 
          pass
      except:
        pass
  
   return render_template('xml.html', title="Генерация")
  else:
    currentclient = Session1.query(Application1).where(Application1.id == request.args.get('id') )

    alluslugi = Session1.query(uslugi1)
    countroom = request.args.get('room')
     
    return render_template('newact.html', data = alluslugi, client =currentclient , title = f"Создание акта для клиента {request.args.get('id')}", element = int(countroom))   

       

def logger(activity, data="Nothing"):
  name = session['familia'] +" "+ session['name'] +" "+ session['otchestvo']
  dat = insert(logging).values(id_name = session['id'],name = name,operation = activity,extra = data)
  with engine.connect() as conn:
    conn.execute(dat)

@app.route('/userslogs?page=<int:page_num>')
@app.route('/userslogs')
def userslogs(page_num=1):
  if session['logged_in'] == True: 
    try:
    #alllogging = logging.query.order_by(logging.id_name.desc()).paginate(per_page=50, page=page_num, error_out=True)
     lastrow = Session1.query(logging).order_by(logging.id.desc()).first()
     firstrow = int(lastrow.id)-599
     alllogging = logging.query.order_by(logging.id.desc()).filter(logging.id>firstrow).paginate(per_page=50, page=page_num, error_out=True)
     return render_template('userlogs.html', data = alllogging, title="Мониторинг активности пользователей")
    except:
     return render_template('userlogs.html', data = alllogging, title="Мониторинг активности пользователей")
  else: 
    return render_template('/auth/login.html', error = "У вас нет доступа, авторизуйтесь", title="Список пользователей")

"""
