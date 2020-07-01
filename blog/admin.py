from django.contrib import admin
# Register your models here.
from .models import Blog



# admin.site.register(ReadNum)

class BlogAdmin(admin.ModelAdmin):
	list_display = ['title', 'id', 'author', 'get_read_num', 'created_time', 'last_updated_time']
	search_fields = ['title']
	
	

class ReadNumAdmin(admin.ModelAdmin):
	list_display = ('read_num', 'blog')
admin.site.register(Blog, BlogAdmin)#把文章模型注册到admin模块 