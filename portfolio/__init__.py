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
  comment = CommentForm()
  return render_template('comment.html', title='Comment',comment=comment)

# @app.route("/comment",methods=['GET','POST'])
# def commentposted():
#   comment = CommentForm()
#   flash('Comment posted!')
#   name = comment.name.data
#   iscomment = comment.comment.data
#   print(name)
#   print(iscomment)
#   return render_template('comment.html',title='Comment',comment=comment)

@app.route("/comment", methods=['GET', 'POST'])
def commentposted():
  comment = CommentForm()
  if comment.validate_on_submit():
    name = comment.name.data
    iscomment = comment.comment.data
    new_comment = Comment(name, iscomment)
    db.session.add(new_comment)
    db.session.commit()
    flash('Comment posted!')
  return render_template('comment.html',title='Comment',comment=comment)

@app.route("/recentcomments")
def recentcomments():
  allcomment = Comment.query.order_by(Comment.date.desc()).all()
  return render_template('recentcomments.html', allcomment=allcomment)

with app.app_context():
  db.create_all()
