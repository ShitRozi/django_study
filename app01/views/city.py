import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import UploadForm, UploadModalForm
from staff_manager import settings


def city_list(request):
    queryset = models.City.objects.all()

    return render(request, 'city_list.html', {'queryset': queryset})


def city_add(request):
    title = '新建城市'
    if request.method == "GET":
        form = UploadModalForm()
        return render(request, "upload_form.html", {'form': form, 'title': title})
    form = UploadModalForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 字段加上传的路径写入到数据库
        form.save()
        return redirect('/city/list/')
    return render(request, 'upload_form.html', {'form': form, 'title': title})
