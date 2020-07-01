import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.db.models import Sum
from django.utils import timezone


def read_statistics_once_read(request, obj):
	ct = ContentType.objects.get_for_model(obj)
	key = '%s_%s_read' % (ct.model, obj.pk)
	if not request.COOKIES.get(key):
		readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
		readnum.read_num += 1
		readnum.save()

		date = timezone.now().date()
		# if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk).count():
		# 	readdetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk,date=date)
		# # else:
		# 	readdetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
		readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
		

		readdetail.read_num += 1
		readdetail.save()
	return key

def get_sever_days_read_data(content_type):
	today = timezone.now().date()#取出日期
	read_nums = []
	dates = []
	for i in range(6, -1, -1):
		date = today - datetime.timedelta(days=i)#日期差量
		dates.append(date.strftime('%m/%d'))
		read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
		result = read_details.aggregate(read_num_sum=Sum('read_num'))
		read_nums.append(result['read_num_sum'] or 0)
	return dates, read_nums


def get_today_hot(content_type):
	today = timezone.now().date()
	read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
	return read_details[:7]#最多现实的条数

def get_yesterday_hot(content_type):
	today = timezone.now().date()
	yesterday = today -datetime.timedelta(days=1)#如果取一周，就-7。
	read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
	return read_details[:7]

