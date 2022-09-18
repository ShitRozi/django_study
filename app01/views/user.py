from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import UserModelForm
from app01.utils.pagination import Pagination


def user_list(request):


    # [obj, obj, obj]
    queryset = models.UserInfo.objects.all()

    page_obj = Pagination(request, queryset)

    # obj.get_gender_display()根据数据库创建时，反choice元组里套元组，django提供的方法
    # obj.depart.title：当有外键是，根据本对象引用创建外键是的名字，ex：depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # 上述外键创建方法django会自动加个_id
    # for obj in queryset:
    #     print(obj.id, obj.name,obj.create_time.strftime("%Y-%m-%d"), obj.get_gender_display(), obj.depart.title)
    context = {'queryset': page_obj.page_queryset, 'page_string': page_obj.html()}

    return render(request, 'user_list.html', context)


def user_add(request):
    """原始方法"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    name = request.POST.get('name')
    age = request.POST.get('age')
    pwd = request.POST.get('pwd')
    depart_id = request.POST.get('dp')
    ctime = request.POST.get('c')
    print(depart_id)
    gender = request.POST.get('gender')
    salary = request.POST.get('salary')

    models.UserInfo.objects.create(name=name, gender=gender,
                                   age=age, depart_id=depart_id,
                                   acccunt=salary, password=pwd,
                                   create_time=ctime,
                                   )
    return redirect('/user/list/')


def user_model_form_add(request):
    """ 添加用户（ModelForm版本）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': '123', 'password': '123', 'age': 11, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: IT运维部门>}
        # print(form.cleaned_data)
        # models.UserInfo.objects.create(..)
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """编辑用户"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据id获取去数据库获取要编辑的数据
        form = UserModelForm(instance=row_object)  # instance=row_object让输入框里默认出现从数据库中得到的数据，达到编辑的效果
        return render(request, 'user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST, instance=row_object)  # 不能不写instance，不然会新增一行，写了之后让django知道要保存到哪一行
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    """删除用户"""
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')