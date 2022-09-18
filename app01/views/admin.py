from django.shortcuts import render, redirect
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from app01 import models
from app01.utils.pagination import Pagination
from django.core.exceptions import ValidationError


def admin_list(request):
    """管理员列表"""

    # 检查用户是否已经登陆，已经登陆继续，没登陆让他登录
    # 用户发来请求，获取cookie中字符串，看看session中有没有
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict['username__contains'] = search_data
    # 根据搜索条件获取数据
    queryset = models.Admin.objects.filter(**data_dict)
    page_obj = Pagination(request, queryset)
    context = {
        "queryset": page_obj.page_queryset,
        'page_string': page_obj.html(),
        'search_data': search_data,
    }
    return render(request, 'admin_list.html', context)


def admin_add(request):
    """新建管理员"""

    title = '新建管理员'
    if request.method == "GET":
        form = AdminModelForm()
        context = {
            'title': title,
            'form': form,
        }
        return render(request, 'change.html', context)
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # form.cleaned_data 里是一个字典，包括验证通过的所有的信息，可以利用这一点查看密码和确认密码是否一致
        # if form.clean_confirm_password():
        #
        #     form.save()
        #     return redirect('/admin/list/')
        # else:
        #     raise ValidationError("密码不一致")

        form.save()
        # for field in form:
        #     print(field)
        print(form.cleaned_data)

        return redirect('/admin/list/')
    # for field in form:
    #     print(field.errors)

    return render(request, 'change.html', {
        'title': title,
        'form': form,
    })


def admin_edit(request, nid):
    """编辑管理员"""

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html')
    # 能获取到nid对应的id对象
    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)  # 编辑模式下显示默认值
        context = {
            'title': title,
            'form': form
        }
        return render(request, 'change.html', context)
    # 不能不写instance，不然会新增一行，写了之后让django知道要保存到哪一行
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'change.html', context)


def admin_delete(request, nid):
    """删除"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    """重置密码"""

    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html')
    # 能获取到nid对应的id对象
    title = "重置密码 - {}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetModelForm()  # 编辑模式下显示默认值
        context = {
            'title': title,
            'form': form
        }
        return render(request, 'change.html', context)
    # 不能不写instance，不然会新增一行，写了之后让django知道要保存到哪一行
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'change.html', context)
