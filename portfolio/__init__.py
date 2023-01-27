from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cw2.db')
app.config['SECRET_KEY'] = '(34879*&378^83hehj3349837rjkhekjfn)'
app.config['SRF_ENABLED'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class CommentForm(FlaskForm):
  name = StringField('Name',validators=[DataRequired()])
  comment = StringField('Comment',validators=[DataRequired()])
  submit = SubmitField('Post Comment')

class PasswordForm(FlaskForm):
  password = StringField('Name',validators=[DataRequired()])
  submit = SubmitField('Submit Password')
  
class Comment(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   name = db.Column(db.String, nullable=False)
   comment = db.Column(db.Text, nullable=False)
  
class Password(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   password = db.Column(db.String, nullable=False)
   
class Project(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   year = db.Column(db.String, nullable=False)
   project_category = db.Column(db.String, nullable=False)
   project_name = db.Column(db.String, nullable=False)
   project_description = db.Column(db.String, nullable=False)

def __repr__(self):
    return f"Comment('{self.name}', '{self.comment}')"

@app.route("/")

@app.route("/index")
def index():
  password = PasswordForm()
  return render_template('index.html', title='Index',form=PasswordForm(password=password))

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def passwordSubmit():
  password = PasswordForm()
  inputPassword = password.password.data
  if(inputPassword == "admin"):
    flash('Welcome!')
    return redirect(url_for("home"))
  else:
    flash('Wrong password')
    return redirect(url_for("index"))

@app.route("/home")
def home():
  return render_template('home.html', title='Home')

@app.route("/about")
def about():
  return render_template('about.html', title='About')

@app.route("/about")
def project_all():
    all_projects = Project.query.all()
    return render_template('about.html', all_projects=all_projects)

@app.route("/about", methods=['GET', 'POST'])
def about_project():
    year = request.form.get('year')
    category = request.form.get('category')
    projects = Project.query
    if year:
        projects = projects.filter(Project.year == year)
    if category:
        projects = projects.filter(Project.project_category == category)
    return render_template('about.html', projects=projects)

@app.route("/comment")
def comment():
  comment = CommentForm()
  recentcomments = Comment.query.order_by(Comment.date.desc()).all()
  return render_template('comment.html', title='Comment',comment=comment,recentcomments=recentcomments)

@app.route("/comment", methods=['GET', 'POST'])
def commentposted():
  comment = CommentForm()
  name = comment.name.data
  iscomment = comment.comment.data
  new_comment = Comment()
  new_comment.name = name
  new_comment.comment = iscomment
  db.session.add(new_comment)
  db.session.commit()
  flash('Comment posted!')
  return redirect(url_for('comment'))
  
@app.route("/comments")
def comments():
  return render_template('recentcomments.html', comment=comment)

with app.app_context():
  db.create_all()
