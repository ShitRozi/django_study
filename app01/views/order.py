from django.shortcuts import HttpResponse, render, redirect

from app01 import models
from app01.utils.form import OrderModelForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import datetime
from app01.utils.pagination import Pagination


def order_list(request):
    queryset = models.Order.objects.all().order_by('-id')
    # 1.根据自己的情况去筛选自己的数据

    # 2.实例化分页对象
    page_object = Pagination(request, queryset)
    form = OrderModelForm()
    context = {
        'form': form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """新建订单----ajax请求"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 动态生成订单id，加入数据库中
        form.instance.oid = datetime.now().strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 管理员
        # form.instance.admin_id = 当前登录用户 此id去session中去获取
        form.instance.admin_id = request.session['info']['id']
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({"status": False, 'error': form.errors})


def order_delete(request):
    """删除订单"""
    uid = request.GET.get('uid')
    if not models.Order.objects.filter(id=uid).exists():
        return JsonResponse({"status": False, 'error': '删除失败，数据不存在'})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def order_detail(request):
    """根据id获取详细订单"""
    # 方案一
    """
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'error': '删除失败，数据不存在'})

    # 从数据库中获取到一个对象 row_object
    row_dict = {
        'title': row_object.title,
        'price': row_object.price,
        'status': row_object.status,
    }
    result = {
        'status': True,
        'data': row_dict,
    }
    return JsonResponse(result)
    """

    # 方案二
    uid = request.GET.get('uid')
    # 直接加个values构造字典
    row_dict = models.Order.objects.filter(id=uid).values('title', 'price', 'status').first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': '数据不存在'})

    # 从数据库中获取到一个对象 row_object
    result = {
        'status': True,
        'data': row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': '数据不存在'})
    form = OrderModelForm(data=request.POST, instance=row_object)

    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})
