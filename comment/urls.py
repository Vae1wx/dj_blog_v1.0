from django.urls import path, re_path
from . import views

urlpatterns = [
	path('update_comment', views.update_comment, name='update_comment'),

]