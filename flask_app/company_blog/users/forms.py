from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

from company_blog.models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email(message="正しいメールアドレスを入力してください")])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('ログイン')

class RegistrationForm(FlaskForm):
	email = StringField('メールアドレス', validators=[DataRequired(), Email(message="正しいメールアドレスを入力してください")])
	username = StringField('ユーザー名', validators=[DataRequired()])
	password = PasswordField('パスワード', validators=[DataRequired(), EqualTo('pass_confirm', message='パスワードが一致しません')])
	pass_confirm = PasswordField('パスワード(確認)', validators=[DataRequired()])
	submit = SubmitField('登録')

	def validate_name(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('そのユーザー名は既に使用されています')
		
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('そのメールアドレスは既に使用されています')
		
class Updateuserforom(FlaskForm):
	email = StringField('メールアドレス', validators=[DataRequired(), Email(message="正しいメールアドレスを入力してください")])
	username = StringField('ユーザー名', validators=[DataRequired()])
	password = PasswordField('パスワード', validators=[EqualTo('pass_confirm', message='パスワードが一致しません')])
	pass_confirm = PasswordField('パスワード(確認)')
	submit = SubmitField('更新')

	def __init__(self, user_id,*args, **kwargs):
		super(Updateuserforom, self).__init__(*args, **kwargs)
		self.id = user_id
	
	def validate_username(self, field):
		if User.query.filter(User.id != self.id).filter_by(username=field.data).first():
			raise ValidationError('そのユーザー名は既に使用されています')
		
	def validate_email(self, field):
		if User.query.filter(User.id != self.id).filter_by(email=field.data).first():
			raise ValidationError('そのメールアドレスは既に使用されています')
