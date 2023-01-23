from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '<182732873917398719371873>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c22021052:Yonghoon1994!@csmysql.cs.cf.ac.uk:3306/c22021052_cw2_db'
db = SQLAlchemy(app)

class CommentForm(FlaskForm):
  name = StringField('Name',validators=[DataRequired()])
  comment = StringField('Comment',validators=[DataRequired()])
  submit = SubmitField('Register')
  
class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  name = db.Column(db.String, nullable=False)
  comment = db.Column(db.Text, nullable=False)

def __repr__(self):
    return f"Comment('{self.name}', '{self.comment}')"

@app.route("/")

@app.route("/home")
def home():
  return render_template('home.html', title='Home')

@app.route("/about")
def about():
  return render_template('about.html', title='About')

@app.route("/comment")
def comment():
  return render_template('comment.html', title='Comment')

@app.route("/comment",methods=['GET','POST'])
def commentposted():
  comment = CommentForm()
  flash('Comment posted!')
  return render_template('comment.html',title='Comment',comment=comment)
