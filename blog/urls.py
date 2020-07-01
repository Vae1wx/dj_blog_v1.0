from django.urls import path, re_path
from . import views,testdb,search,search2

urlpatterns = [
	path('', views.blog_list, name='blog_list'),#列表页
	re_path(r'^index$', views.add_emp),#练习页
	re_path(r'^mysite$', views.mysite),#练习页
	# re_path(r'^testdb$', testdb.testdb),
	re_path(r'^search_form$', search.search_form),#练习页
    re_path(r'^search$', search.search),#练习页
    re_path(r'^search-post$', search2.search_post),#练习页
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),#博客文章页

    # re_path(r'^content$', views.blog_detail)正则形式url
    #path('type/<int:blog_type_pk', views.blogs_with_type, name='blogs_with_type'),#有bug，暂时不开
   
]