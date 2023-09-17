import numpy as np
import pickle
from flask import Flask, url_for, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
import base64
import tensorflow as tf
from PIL import Image 
import cv2
import io
from keras.models import load_model
import h5py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hackathon_1shg_user:xf83AoqlmOiElqW3rgzgG4PhRG7oH6kQ@dpg-cjp2hlm1208c73c714tg-a.singapore-postgres.render.com:5432/sih'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gauravvermaa07076@gmail.com'
app.config['MAIL_PASSWORD'] = 'reiqgeaklkpiadxe'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
mail = Mail(app)

heart_model = pickle.load(open('model/heart_disease_model.pkl','rb'))
covid_model = load_model('model/covid.model')
liver_model = pickle.load(open('model/liver_model.pkl','rb'))
asd_model = pickle.load(open('model/asd_model.pkl','rb'))
diabetes_model = pickle.load(open('model/diabetes_model.pkl','rb'))


label_dict={0:'Covid19 Negative', 1:'Covid19 Positive'}
img_size = 100

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    patients = db.relationship('Patient', backref='doctor_user')

    def init(self, username, password):
        self.username = username
        self.password = password

# class Patient(db.model)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    age = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    liver_disease = db.Column(db.Integer,default=0)
    heart_disease = db.Column(db.Integer,default=0)
    diabetes = db.Column(db.Integer,default=0)


def predict(model,values,dic):
    values = np.asarray(values)
    return model.predict(values.reshape(1, -1))[0]


def preprocess(img):

	img=np.array(img)

	if(img.ndim==3):
		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	else:
		gray=img

	gray=gray/255
	resized=cv2.resize(gray,(img_size,img_size))
	reshaped=resized.reshape(1,img_size,img_size)
	return reshaped


#url
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        
        if data is not None:
            session['logged_in'] = True
            session['email'] = data.username
            return redirect(url_for('admin'))
        return render_template('login.html', message="Incorrect Details! If not registered.. Please first do so!")
   
    
@app.route('/admin',methods=['GET','POST'])
def admin():
    return render_template('admin.html')
    # try:
    #     print(session.get("email"))
    # except Exception as e:
    #     print(e) 
    
    # if request.method == 'GET':
    #     return render_template('patient.html')
    


    # doctor_id = User.query.filter_by(username=session.get("email")).first().id
    # print(doctor_id)
    # email = request.form['email']
    # name = request.form['name']
    # age = request.form['age']
    # phone = request.form['phone']

    # db.session.add(Patient(doctor=doctor_id,email=email, name=name,age=age,phone=phone))
    # db.session.commit()

    # return {"message":"patient created"}

@app.route('/uploadpatient',methods=['GET','POST'])
def uploadpatient():
    try:
        print(session.get("email"))
    except Exception as e:
        print(e) 
    
    if request.method == 'GET':
        return render_template('uploadpatient.html')
    


    doctor_id = User.query.filter_by(username=session.get("email")).first().id
    print(doctor_id)
    email = request.form['email']
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']

    db.session.add(Patient(doctor=doctor_id,email=email, name=name,age=age,phone=phone))
    db.session.commit()

    return {"message":"patient created"}

    
@app.route('/patients',methods=['GET','POST'])
def patients():
    doctor_id = User.query.filter_by(username=session.get("email")).first()
    patients = doctor_id.patients
    print(patients)
    return render_template('patients.html',patients = patients)

if __name__ == '__main__':
    app.run(debug=True,port=5002)
