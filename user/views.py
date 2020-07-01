from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls  import reverse
from user.forms import LoginForm, RegForm, ChangeNicknameForm, EmailForm, ChangePassword, ForgetPassword
from .models import Profile
from django.core.mail import send_mail
from django.http import JsonResponse
import string, random, time
from django.conf import settings
# Create your views here.


def login(request):
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			auth.login(request, user)
			return redirect(request.GET.get('from', reverse('home')))
	else:
		login_form = LoginForm()
	context = {}
	context['login_form'] = login_form
	return render(request, 'login.html', context)

def register(request):
	if request.method == 'POST':
		reg_form = RegForm(request.POST)
		if reg_form.is_valid():
			username = reg_form.cleaned_data['username']
			email = reg_form.cleaned_data['email']
			password = reg_form.cleaned_data['password']
			# 创建用户
			user = User.objects.create_user(username, email, password)
			user.save()
			# 清楚session
			del request.session['register_code']
			# 登录
			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
			return redirect(request.GET.get('from', reverse('home')))
	else:
		reg_form = RegForm()
	context = {}
	context['reg_form'] = reg_form
	return render(request, 'register.html', context)

def logout(request):
	auth.logout(request)
	return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
	return render(request, 'user_info.html')

def change_nickname(request):
	if request.method == 'POST':
		form = ChangeNicknameForm(request.POST, user=request.user)
		if form.is_valid():
			nickname_new = form.cleaned_data['nickname_new']
			profile, created = Profile.objects.get_or_create(user=request.user)
			profile.nickname = nickname_new
			profile.save()
			return redirect(request.GET.get('from', reverse('home')))
	else:
		form = ChangeNicknameForm()

	context = {}
	context['form'] = form
	context['page_title'] = '修改昵称'
	context['form_title'] = '修改昵称'
	context['submit_text'] = '修改'
	context['return_back_url'] = request.GET.get('from', reverse('home'))
	return render(request, 'form.html', context)

def email(request):
		if request.method == 'POST':
			form = EmailForm(request.POST, request=request)
			if form.is_valid():
				email = form.cleaned_data['email']
				request.user.email = email
				request.user.save()
				# 清楚session
				del request.session['email_code']
				return redirect(request.GET.get('from', reverse('home')))
		else:
			form = EmailForm()

		context = {}
		context['form'] = form
		context['page_title'] = '绑定邮箱'
		context['form_title'] = '绑定邮箱'
		context['submit_text'] = '绑定'
		context['return_back_url'] = request.GET.get('from', reverse('home'))
		return render(request, 'form.html', context)

def send_verification_code(request):
	email = request.GET.get('email', '')# 先接受前端传的邮箱账号，账号可以为空。
	data = {}
	if email != '':
		# 生成验证码
		code = ''.join(random.sample(string.ascii_letters + string.digits, 4))# 生成的四个随机字母，变成列表形式。
		now_time = int(time.time())
		send_code_time = request.session.get('send_code_time', 0)
		if now_time - send_code_time < 30:
			data['status'] = 'ERROR'
		else:
			request.session['verification_code'] = code
			request.session['send_code_time'] = now_time
			send_mail('薛定谔的验证码', 
				settings.EMAIL_HOST_USER,
				 '1103913822@qq.com',
				  [email],
				  fail_silently = False)
			data['status'] = 'SUCCESS'
	else:
		data['status'] = 'ERROR'
	return JsonResponse(data)

def change_password(request):
	if request.method == 'POST':
		form = ChangePassword(request.POST, user=request.user)
		if form.is_valid():
			user = request.user
			new_password = form.cleaned_data['new_password']
			user.set_password(new_password)
			user.save() # 保存
			auth.logout(request) # 登出
			return redirect(request.GET.get('from', reverse('home')))
	else:
		form = ChangePassword()

	context = {}
	context['form'] = form
	context['page_title'] = '修改昵称'
	context['form_title'] = '修改昵称'
	context['submit_text'] = '修改'
	context['return_back_url'] = request.GET.get('from', reverse('home'))
	return render(request, 'form.html', context)

def forget_password(request):
	if request.method == 'POST':
		form = ForgetPassword(request.POST, request=request)
		if form.is_valid():
			email = form.cleaned_data['email']
			new_password = form.cleaned_data['new_password']
			user = User.objects.get(email=email)
			user.set_password(new_password)
			user.save() # 保存

			del request.session['verification_code']
			return redirect(reverse('home'))
	else:
		form = ForgetPassword()

	context = {}
	context['form'] = form
	context['page_title'] = '忘记密码'
	context['form_title'] = '修改密码'
	context['submit_text'] = '修改'
	context['return_back_url'] = reverse('home')
	return render(request, 'form.html', context)