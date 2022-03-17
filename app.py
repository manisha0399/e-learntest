
from flask import Flask, render_template, request,session,redirect,flash,url_for,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from flask import Flask,  request
import re
from flask_migrate import Migrate 

app = Flask(__name__,template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uvcewhbbqtkmml:e38eadfffca0476eed909f2a21aecdef0f76165f43b8ee4a5d9235d769ede864@ec2-34-224-226-38.compute-1.amazonaws.com:5432/dum2phlj6sumi'



ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uvcewhbbqtkmml:e38eadfffca0476eed909f2a21aecdef0f76165f43b8ee4a5d9235d769ede864@ec2-34-224-226-38.compute-1.amazonaws.com:5432/dum2phlj6sumi'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Register(db.Model):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    uname = db.Column(db.String(200))
    email = db.Column(db.String(200),unique=True)
    password =db.Column(db.String(10))
    cpassword =db.Column(db.String(10))

    def __init__(self, name, uname, email, password, cpassword):
        self.name = name
        self.uname = uname
        self.email = email
        self.password = password
        self.cpassword = cpassword


@app.route("/")
def Home():
    return render_template('index.html')

@app.route("/about")
def About():
    return render_template('about.html')

@app.route("/album")
def Album():
    return render_template('album.html')



@app.route("/register", methods=['GET','POST'])
def register():
    if(request.method=='POST'):
        name = request.form.get('name')
        uname = request.form.get('uname')
        email= request.form.get('email')
        password= request.form.get('password')
        cpassword= request.form.get('cpassword')

        if name == '' or uname == '' or email == '' or password == '' or cpassword == '':
            return render_template('register.html', message='Please enter required fields')
        if db.session.query(register).filter(register.email == email).count() == 0:
            data = register(name, uname, email, password,cpassword)
            db.session.add(data)
            db.session.commit()
            
            return render_template('success.html')
    return render_template('register.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if (request.method== "GET"):
        if('email' in session and session['email']):
            return render_template('dashboard.html')
        else:
            return render_template("login.html")

    if (request.method== "POST"):
        email = request.form["email"]
        password = request.form["password"]
        
        login = Register.query.filter_by(email=email, password=password).first()
        if login is not None:
            session['email']=email
            return render_template('dashboard.html')
        else:
            flash("plz enter right password",'error')
            return render_template('login.html')

@app.route("/contact",  methods=['GET','POST'])
def contact():
    if(request.method =='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        subject=request.form.get('subject')
        message=request.form.get('message')
        entry=Contact(name=name,email=email,subject=subject,message=message)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

@app.route("/web",methods=['GET','POST'])
def web_development():
    return render_template('web.html')

@app.route("/andriod",methods=['GET','POST'])
def andriod_development():
    return render_template('andriod.html')

@app.route("/art",methods=['GET','POST'])
def Art():
    return render_template('art.html')

@app.route("/photography",methods=['GET','POST'])
def Photography():
    return render_template('photography.html')

@app.route("/uxdesign",methods=['GET','POST'])
def Uxdesign():
    return render_template('uxdesign.html')

@app.route("/graphic",methods=['GET','POST'])
def Graphic_design():
    return render_template('graphic.html')

@app.route("/marketing",methods=['GET','POST'])
def Digital_marketing():
    return render_template('marketing.html')

@app.route("/linux",methods=['GET','POST'])
def Linux_development():
    return render_template('linux.html')

@app.route("/web_development")
def download_file():
    p="website_development_tutorial.pdf"
    return send_file(p,as_attachment=True)

@app.route("/andriod_development")
def andriod_download_file():
    c="android_tutorial.pdf"
    return send_file(c,as_attachment=True)

@app.route("/art_craft")
def art_download_file():
    d="art_and_design-_a_comprehensive_guide_for_creative_artists.pdf"
    return send_file(d,as_attachment=True)

@app.route("/photo")
def photo_download_file():
    m="photography.pdf"
    return send_file(m,as_attachment=True)

@app.route("/ux")
def ux_download_file():
    k="ux design.pdf"
    return send_file(k,as_attachment=True)

@app.route("/graphics")
def graphics_download_file():
    n="Graphic Design.pdf"
    return send_file(n,as_attachment=True)

@app.route("/digital")
def digital_download_file():
    s="Digital Marketing.pdf"
    return send_file(s,as_attachment=True)

@app.route("/linux_development")
def linux_download_file():
    a="Linux development.pdf"
    return send_file(a,as_attachment=True)

@app.route("/adminlogin",methods=['GET','POST'])
def adminlogin():
    if(request.method=='POST'):
        email=request.form.get('email')
        password=request.form.get('password')
        if email=='admin@gmail.com' and password=='123456':
            return render_template('admindash.html') 
    return render_template('adminlogin.html')



@app.route("/logout", methods = ['GET','POST'])
def logout():
    session.pop('email')
    return redirect(url_for('Home')) 


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.debug = True
    app.run()