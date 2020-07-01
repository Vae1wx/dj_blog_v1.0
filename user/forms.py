from django import forms
from django.core.exceptions import ValidationError
from blog import models
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(label='账号', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
	password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		user = auth.authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError('用户名或密码错误')
		else:
			self.cleaned_data['user'] = user
		return self.cleaned_data

class RegForm(forms.Form):
	username = forms.CharField(label='用户名', max_length=30, min_length=2, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
	password_again = forms.CharField(label='密码', max_length=10, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
	password = forms.CharField(label='再次输入密码', max_length=10, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再次输入密码'}))
	email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
	verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'点击“发送验证码”到邮箱'}))#验证码

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('用户名已存在')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('邮箱已使用')
		return email

	def clean_password(self):
		password = self.cleaned_data['password']
		password_again = self.cleaned_data['password_again']
		if password != password_again:
			raise forms.ValidationError('两次输入不一致')
		return password_again

	def clean(self):
		# 判断验证码
		code = self.request.session.get('verification_code', '')
		verification_code = self.cleaned_data.get('verification_code', '')
		if code == '' and code != verification_code:
			raise forms.ValidationError('验证码不正确')
		return self.cleaned_data


class ChangeNicknameForm(forms.Form):
	nickname_new = forms.CharField(label='新的昵称',
		max_length = 20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入新的昵称'}))

	def __init__(self, *args, **kwargs):
		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		super(ChangeNicknameForm, self).__init__(*args, **kwargs)

	def clean(self):
		# 判断用户是否登录
		if self.user.is_authenticated:
			self.cleaned_data['user'] = self.user
		else:
			raise forms.ValidationError('用户尚未登录')
		return self.cleaned_data
	def clean_nickename_new(self):

		nickename_new = self.cleaned_data.get('nickename_new', '').strip()
		if nickename_new == '':
			raise forms.ValidationError('昵称不能为空')
		return nickename_new
class EmailForm(forms.Form):
	email = forms.EmailField(label='邮箱', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
	verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'点击“发送验证码”到邮箱'}))#验证码
	

	def __init__(self, *args, **kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(EmailForm, self).__init__(*args, **kwargs)

	def clean(self):
		# 判断用户是否登录
		if self.request.user.is_authenticated:
			self.cleaned_data['user'] = self.request.user
		else:
			raise forms.ValidationError('用户尚未登录')
		# 判断用户是否已绑定邮箱
		if self.request.user.email != '':
			raise forms.ValidationError('已绑定')
		# 判断验证码
		code = self.request.session.get('verification_code', '')
		verification_code = self.cleaned_data.get('verification_code', '')
		if code == '' and code != verification_code:
			raise forms.ValidationError('验证码不正确')
		return self.cleaned_data

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('该邮箱已被使用')
		return email

	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code', '').strip()
		if verification_code == '':
			raise forms.ValidationError('验证码不能为空')
		return verification_code

class ChangePassword(forms.Form):
	old_password = forms.CharField(label='旧的密码', max_length=10, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入旧密码'}))
	new_password = forms.CharField(label='新的密码', max_length=10, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入新密码'}))
	new_password_again = forms.CharField(label='再次输入新的密码', max_length=10, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再次输入新密码'}))

	def clean(self):
		# 新的密码是否一致
		new_password = self.cleaned_data['new_password']
		new_password_again = self.cleaned_data['new_password_again']
		if new_password != new_password_again:
			raise forms.ValidationError('两次输入不一致')
		return self.cleaned_data

	def __init__(self, *args, **kwargs):  # 获取到user 已登录后可以用于验证旧密码
		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		super(ChangePassword, self).__init__(*args, **kwargs)

	def clean_old_password(self):
		# 旧密码是否正确
		old_password = self.cleaned_data.get('old_password', '')
		if not self.user.check_password(old_password):
			raise forms.ValidationError('旧的密码错误')
		return old_password

class ForgetPassword(forms.Form):
	username = forms.CharField(label='账号', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
	email = forms.EmailField(label='邮箱', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
	verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'点击“发送验证码”到邮箱'}))#验证码
	new_password = forms.CharField(label='新的密码', max_length=10, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入新密码'}))
	new_password_again = forms.CharField(label='再次输入新的密码', max_length=10, min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请再次输入新密码'}))

	def clean(self):
		# 新的密码是否一致
		new_password = self.cleaned_data['new_password']
		new_password_again = self.cleaned_data['new_password_again']
		if new_password != new_password_again:
			raise forms.ValidationError('两次输入不一致')
		return self.cleaned_data

	def clean_usename(self):
		username = self.cleaned_data['username'].strip()
		if not User.objects.filter(username=username).exists():# 如果用户名不存在
			raise forms.ValidationError('用户名输入错误或不存在')


	def __init__(self, *args, **kwargs):  # 获取到user 已登录后可以用于验证旧密码
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(ForgetPassword, self).__init__(*args, **kwargs)


	def clean_verification_code(self):
		verification_code = self.cleaned_data.get('verification_code', '').strip()
		if verification_code == '':
			raise forms.ValidationError('验证码不能为空')
		return verification_code


		code = self.request.session.get('verification_code', '')
		verification_code = self.cleaned_data.get('verification_code', '')
		if code == '' and code != verification_code:
			raise forms.ValidationError('验证码不正确')
		return self.cleaned_data