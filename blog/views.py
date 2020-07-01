import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from .models import Blog
from django.db.models import Sum
from django.core.paginator import Paginator#分页
from django.utils import timezone
from read_statistics.models import ReadNum
from read_statistics.tools import read_statistics_once_read, get_sever_days_read_data, get_today_hot
from django.core.cache import cache  #缓存
from comment.models import Comment

# Create your views here.


def index(request):
	return HttpResponse('Hello,world!')

def get_7_days_hot_blogs():
	today = timezone.now().date()
	week = today -datetime.timedelta(days=7)
	blogs = Blog.objects\
				.filter(read_details__date__lt=today, read_details__date__gte=week)\
				.values('id','title')\
				.annotate(read_num_sum=Sum('read_details__read_num'))\
				.order_by('-read_num_sum')# \是换行符 values 分组
	return blogs[:7]

def blog_home(request):
	import datetime
	now = datetime.datetime.now()
	blog_content_type = ContentType.objects.get_for_model(Blog)
	dates, read_nums = get_sever_days_read_data(blog_content_type)
	today_hot = get_today_hot(blog_content_type)
	#获取七天热门博客缓存。
	weekday_hot_cache = cache.get('hot_blogs_for_weekday')
	if weekday_hot_cache is None:
		weekday_hot_cache = get_7_days_hot_blogs()
		cache.set('hot_blogs_for_weekday', weekday_hot_cache, 3600)#第一个参数是缓存的内容，第三个参数是时间，单位是秒。


	context = {}
	context['read_nums'] = read_nums
	context['dates'] = dates
	context['n'] = now
	context['today_hot'] = today_hot
	context['hot_blogs_for_weekday'] = get_7_days_hot_blogs
	return render(request, 'home.html', context)

def mysite(request):
	context= 'Hello world!'
	view_name = ''
	num = 2020
	views_list = ["菜鸟教程1","菜鸟教程2","菜鸟教程3"]
	views_dict = {"name":"菜鸟教程"}
	view_list = ["菜鸟教程","菜鸟教程1","菜鸟教程2","菜鸟教程3",]
	import datetime
	now = datetime.datetime.now()
	views_str = "<a href='https://www.runoob.com/'>点击跳转</a>"
	return render(request, 'index.html', {'context': context,
											'h': view_name,
											'views_dict': views_dict,
											'v': num,
											'n': now,
											'wb': views_str,
											'vl': view_list,
											"views_list": views_list})
def mytest(request):
	view_name = 'hello boy'
	return render(request, 'index.html', {'h': view_name})

	return HttpResponse(return_str)
def blog_list(request):
	blogs_all_list = Blog.objects.all()#全部的博客列表
	page_cut = 4
	paginator = Paginator(blogs_all_list, page_cut)#全部的博客列表，每x篇进行分页
	page_num = request.GET.get('page', 1)#获取页面参数(GET请求)
	page_of_blogs = paginator.get_page(page_num)
	#paginator.page_range #原本的页码范围。全部的
	
	currentr_page_num = page_of_blogs.number #获取当前页
	#前两页就是-2和-1。后两页同理。
	#page_range = [x for x in range(int(page_num) - 2 , int(page_num) + 3) if 0 < x < paginator.num_pages]这句是上面的这行的另一种写法：
	page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages)+1))
	#range(max(currentr_page_num - 2, 1), currentr_page_num)
	
	#range是页码取值范围。max函数用来和页码1比较最大值。当前页最小是1,1-2的值和max的第二个参数相比，取最大值。
	last_page = (blogs_all_list.count() + page_cut - 1) // page_cut
	#补齐页码
	if last_page > 5:
		if currentr_page_num < 2: 
			page_range.append(currentr_page_num + 3)
			if last_page >= 5:
				if currentr_page_num <= 1:
					page_range.append(currentr_page_num + 4)
				elif currentr_page_num == 2: 
					page_range.append(currentr_page_num + 3)

		if last_page - currentr_page_num == 0:
				page_range.insert(0, last_page - 3)
		if last_page >= 5:		
			if last_page - currentr_page_num <= 1:
					page_range.insert(0, last_page - 4)
 
	context = {}
	context['blogs'] = page_of_blogs.object_list
	context['page_of_blogs'] = page_of_blogs
	# context['a'] = Blog.objects.all().count()
	context['page_range'] = page_range
	context['last_page'] = last_page
	return render(request, 'blog_list.html', context)
def blog_detail(request, blog_pk):
	blog = get_object_or_404(Blog, pk=blog_pk)
	read_cookie_key = read_statistics_once_read(request, blog)
	blog_content_type = ContentType.objects.get_for_model(blog)
	
	context = {}
	context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
	context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
	context['blog'] = blog 

	# 									这里已经获取到的blog_content_type是一个字符串，加model变成模型的一个字符串。
	response = render(request, 'blog_detail.html', context)
	response.set_cookie(read_cookie_key, 'true', max_age=60)#或者expires=datetime
	return response
	
def blogs_with_type(request, blog_type_pk):
	context = {}
	blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
	context['blogs'] = Blog.objects.filter(blog_type=blog_type)
	context['blog_type'] = blog_type
	return render(request, 'blogs_with_type.html', context)


#___________________________________
def add_emp(request):
    if request.method == "GET":
        form = EmpForm()
        return render(request, "add_emp.html", {"form": form})
    else:
        form = EmpForm(request.POST)
        if form.is_valid():  # 进行数据校验
            # 校验成功
            data = form.cleaned_data  # 校验成功的值，会放在cleaned_data里。
            data.pop('r_salary')
            print(data)

            models.Emp.objects.create(**data)
            return HttpResponse(
                'ok'
            )
            # return render(request, "add_emp.html", {"form": form})
        else:
            print(form.errors)    # 打印错误信息
            clean_errors = form.errors.get("__all__")
            print(222, clean_errors)
        return render(request, "add_emp.html", {"form": form, "clean_errors": clean_errors})

