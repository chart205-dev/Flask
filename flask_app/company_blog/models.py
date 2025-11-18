from datetime import datetime
from pytz import timezone
from werkzeug.security  import check_password_hash, generate_password_hash
from flask_login import UserMixin

from company_blog import db, login_manager

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

class  User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	administrator = db.Column(db.String(1))
	post = db.relationship('BlogPost', backref='author', lazy='dynamic')

	def __init__(self, email, username, password, administrator):
		self.email = email
		self.username = username
		self.password = password
		self.administrator = administrator
	
	def __repr__(self):
		return f"UserName : {self.username}"
	
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def is_administrator(self):
		if self.administrator == "1":
			return 1
		else:
			return 0
	
class BlogPost(db.Model):
	__tablename__ = 'blogposts'
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('users.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id'))
	data = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))
	title = db.Column(db.String(128))
	text = db.Column(db.Text)
	summary = db.Column(db.String(256))
	featured_image = db.Column(db.String(256))

	def __init__(self, userid, category_id, title, text, summary, featured_image):
		self.userid = userid
		self.category_id = category_id
		self.title = title
		self.text = text
		self.summary = summary
		self.featured_image = featured_image
	
	def __repr__(self):
		return f"PostID: {self.id},  Title: {self.title}, Author: {self.author}\n"
	
class BlogCategory(db.Model):
	__tablename__ = "blog_category"
	id = db.Column(db.Integer, primary_key = True)
	category = db.Column(db.String(256))
	posts = db.relationship('BlogPost', backref='blogcategory', lazy='dynamic')

	def __init__(self, category):
		self.category = category

	def __repr__(self):
		return f"CategoryID: {self.id}, CategoryName: {self.category}"


class Inquiry(db.Model):
	__tablename__ = 'inquiry'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	email = db.Column(db.String(64))
	title = db.Column(db.String(128))
	text = db.Column(db.Text)
	date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))

	def __init__(self, name, email, title, text, date):
		self.name = name
		self.email = email
		self.title = title
		self.text = text
		self.date = date

	def __repr__(self):
		return f"InquiryID: {self.id}, Name:{self.name}, Text:{self.text} \n"


