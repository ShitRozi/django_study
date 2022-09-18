from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from app01.utils.pagination import Pagination
from app01 import models
from app01.utils.form import TaskModelForm
from django.http import JsonResponse


def task_list(request):
    """任务列表"""

    # 去数据库获取所有任务

    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = TaskModelForm()
    context = {'form': form, "queryset": page_object.page_queryset, "page_string": page_object.html()}

    return render(request, "task_list.html", context)


# 直接post请求可能会被拒绝，需要加一个@csrf_exempt，免除csrf_token认证
@csrf_exempt
def task_ajax(request):
    """测试ajax"""
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, 'data': [11, 22, 33, 44]}
    # return HttpResponse(json.dumps(data_dict))
    return JsonResponse(data_dict)


@csrf_exempt
def task_add(request):
    # {'level': ['1'], 'title': ['sdfsdfsdfsd'], 'detail': ['111'], 'user': ['8']}
    # print(request.POST)

    # 1.用户发送过来的数据进行校验（ModelForm进行校验）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
