from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

# class Article(models.Model):
# 	name = models.CharField(max_length=20)
# 	article_id = models.AutoField(primary_key=True)
# 	#文章标题
# 	title = models.TextField()
# 	#文章摘要
# 	brief_content = models.TextField()
# 	#文章主要内容
# 	content = models.TextField()
# 	time = models.DateTimeField(auto_now=True)
# 	def __str__(self):
# 		return self.title
# class Test(models.Model):
#     name = models.CharField(max_length=20)

class BlogType(models.Model):
	tpye_name = models.CharField(max_length=15)
	"""docstring for B"""
	def __str__(self):
		return self.type_name

class Blog(models.Model, ReadNumExpandMethod):
	title = models.CharField(max_length=50)
	blog_type = models.CharField(max_length=20)
	content = RichTextUploadingField()
	author = models.TextField(User)
	read_details = GenericRelation(ReadDetail)#只是关联，不会添加到数据库中。
	# read_num = models.IntegerField(default=0)
	created_time = models.DateTimeField(auto_now_add=True)
	last_updated_time = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.title

		
	class Meta:
		ordering = ['-created_time']
# class ReadNum(models.Model):
# 	read_num = models.IntegerField(default=0)
# 	blog = models.OneToOneField(Blog, on_delete=models.CASCADE)

# 	def __str__(self):
# 		return self.blog
