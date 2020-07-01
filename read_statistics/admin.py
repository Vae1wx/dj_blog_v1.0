from django.contrib import admin
from .models import ReadNum, ReadDetail
# Register your models here.


class ReadNumAdmin(admin.ModelAdmin):
	list_display = ('read_num', 'content_object')
admin.site.register(ReadNum)#把文章模型注册到admin模块 
# @admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
	list_display = ('date', 'read_num', 'content_object')
	
admin.site.register(ReadDetail)