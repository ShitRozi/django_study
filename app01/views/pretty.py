from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import PrettyModelForm, PrettyModelFormEdit
from app01.utils.pagination import Pagination


def pretty_list(request):
    """靓号列表"""



    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict['mobile__contains'] = search_data
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    # 实例化类
    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile='13505207854', price=9999, status=2, level=2)

    # 第1页
    # queryset = models.PrettyNum.objects.all()[0:10]
    # 得到数据库总数据数

    # 以level倒叙排列
    # queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[page_object.start:page_object.end]

    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    """新建靓号"""
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_add.html', {"form": form})


def pretty_edit(request, nid):
    """编辑靓号"""
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyModelFormEdit(instance=row_object)

        return render(request, 'pretty_edit.html', {"form": form})

    form = PrettyModelFormEdit(instance=row_object, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request, nid):
    """删除靓号"""
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
