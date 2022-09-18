from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from app01.utils.form import UploadForm, UploadModalForm
import os
from app01 import models
from django.conf import settings


def upload_list(request):
    if request.method == "GET":
        return render(request, 'upload_list.html')
    # request.FILES 请求提交过来的文件

    file_object = request.FILES.get('avatar')
    file_name = file_object.name
    f = open(file_name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)

    f.close()
    return HttpResponse('...')


def upload_form(request):
    title = "Form上传"
    if request.method == "GET":
        form = UploadForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})
    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # print(form.cleaned_data)
        image_object = form.cleaned_data.get('img')
        # 1.读取图片内容写入文件夹中并获取文件路径
        media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)

        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        # 2.将图片文件路径存入数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )

        return HttpResponse('提交成功')
    return render(request, 'upload_form.html', {'form': form, 'title': title})


def upload_modal_form(request):
    """modal_form上传数据"""
    title = "Modal Form上传文件"
    if request.method == "GET":
        form = UploadModalForm()
        return render(request, "upload_form.html", {'form': form, 'title': title})
    form = UploadModalForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 字段加上传的路径写入到数据库
        form.save()
        return HttpResponse("成功")
    return render(request, 'upload_form.html', {'form': form, 'title': title})
