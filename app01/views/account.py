from django.shortcuts import render, redirect, HttpResponse
from app01.utils.form import LoginForm
from app01 import models
from app01.utils.code import check_code
from io import BytesIO


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context)
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，不能用save（）
        print(form.cleaned_data)
        # return HttpResponse("登陆成功")

        admin_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if admin_input_code.upper() != code.upper():
            form.add_error('code', '验证码错误')  # 主动抛出错误
            context = {
                'form': form
            }
            return render(request, 'login.html', context)

        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password', '用户名或密码错误')  # 主动抛出错误
            context = {
                'form': form
            }
            return render(request, 'login.html', context)
        # 用户名密码正确
        # 网站生成一个随机字符串，写道用户浏览器的cookie中，再写入session中
        request.session['info'] = {
            'id': admin_object.id,
            'name': admin_object.username,
        }

        # 重新设置session超时时间
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/admin/list/')

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def logout(request):
    """注销"""

    # 清除session
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    """生成图片验证码"""
    # 调用code生成函数
    img, code_string = check_code()
    # 写入session中以便后续获取验证码进行校验
    request.session['image_code'] = code_string
    # 设置60秒超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())
