from flask import Flask, session,render_template, request, redirect, g, send_from_directory
import time
from sqlalchemy.dialects.postgresql import UUID
import json
from flask_login import LoginManager, UserMixin,logout_user, login_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_url_path='')

#create_engine('sqlite:///C:\\path\\to\\foo.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/files') #'/uploads/files'

#engine = create_engine('sqlite:///E:\\GreivancePortal\\portal.db')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, unique = True, primary_key = True)
    #id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    name = db.Column(db.String(32))
    email = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(32))

class Grievance(db.Model):
    g_id =db.Column(db.Integer, unique = True, primary_key = True)
    g_type=db.Column(db.String(200),nullable=False)
    institute=db.Column(db.String(200),nullable=False)
    content=db.Column(db.String(2000),nullable=False)
    feedback=db.Column(db.String(200))
    status=db.Column(db.String(200))
    mood=db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods = ["GET"])
def index():
    if current_user.is_authenticated:
         return render_template("main.html")
    else:
         return render_template("index.html")

@app.route('/login', methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email = email).first()
    if check_password_hash(user.password, password):
        login_user(user)
    
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()    
    return redirect('/')

@app.route('/register', methods = ['POST'])
def register():
    if current_user.is_authenticated:
        logout_user()
    
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password']
    name = request.form['name']

    user = User()

    user.email = email
    user.password = generate_password_hash(password)
    user.name = name

    db.session.add(user)
    db.session.commit()

    return redirect('/')


@app.route('/submitgrievance', methods = ['POST'])
@login_required
def submit():
    form = request.get_json()
    new_g = {'user':form['user'],
             'type': form['type'], 
             'department':form['department'], 
             'text':form['text'], 
             'mood':None, 
             }

    greivance.append(new_g)
    return "Your Grievance has been submitted"


@app.route('/uploadtest', methods = ['POST'])
def upload():
    if request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #return redirect(url_for('uploaded_file', filename=filename))
        return 'okay'

if __name__ == '__main__':
    app.debug = True
    app.run(port = 3000)
    
