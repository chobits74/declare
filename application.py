import pymysql 
from flask import Flask,render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


from datetime import datetime
application = Flask(__name__)
#config
#app.config['START_NGROK'] = not None 
#app.config['WERKZEUG_RUN_MAIN'] = False
application.config['SECRET_KEY'] = "secret Admirer"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
application.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://admin:admin1234@declare-1.cqzbw5yjth0y.ap-southeast-1.rds.amazonaws.com:3306/declare-1'
SQLALCHEMY_POOL_RECYCLE = 3600
db = SQLAlchemy(application)


#model
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, default=datetime.now)
    matric = db.Column(db.String(100), nullable=False)
    #due = db.Column(db.Date,nullable = True, default=datetime.now) 
    done = db.Column(db.Boolean)
    #add type of assessment in the class
    asmntType = db.Column(db.String(100), nullable=False)

#create constructor
def __init__(self, name,done,matric,asmntType):
    self.name = name
    #add if task is done
    self.done = done
    self.matric = matric
    #new constructor
    self.asmntType = asmntType

@application.route('/')
def index():
    data_list = Data.query.all()
    

    #creating collection of assessment using dictionary

    asmntType = {"PT1","PT2", "PT3", "PT4", "PE1", "PE2", "PE3", "PE4", "CS", "PBT", "PBTPresnt"}
    
    return render_template('data.html', data_list = data_list, asmntType = asmntType)

@application.route('/insert', methods =['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        matric = request.form['matric']
        #add new field
        asmntType = request.form['asmntType']
         #using html form not flask wtf form
        #due = request.form['due']   
          
#constructor
        my_data = Data(name=name, matric=matric, done=False , asmntType = asmntType)
        db.session.add(my_data)
        db.session.commit()
        return redirect (url_for('index'))

@application.route('/done/<int:todo_id>', methods = ['POST', 'GET'])
def done(todo_id):
    todo = Data.query.filter_by(id=todo_id).first()
    todo.done = not todo.done
    db.session.commit()
    #db.session.close()
    return redirect (url_for('index'))
 
# @app.route('/form')
# def form():
#     return render_template('form.html')
 
# @app.route('/data', methods = ['POST', 'GET'])
# def data():

#     if request.method == 'GET':
#         return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#     if request.method == 'POST':
#         form_data = request.form
#         return render_template('data.html',form_data = form_data)


db.create_all()
 
if __name__ == '__main__':
	db.create_all()
	application.run(host='localhost', port=5000)

    





