from user.forms import LoginForm

def get_login_form(request):
	return {'get_login_form': LoginForm()}