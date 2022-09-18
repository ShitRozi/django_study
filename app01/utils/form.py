from app01.utils.bootstrap import BootStrapModelForm, BootstrapForm
from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
from app01.utils.encrypt import md5


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }


class PrettyModelForm(BootStrapModelForm):
    # 验证手机号格式方式1
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机格式错误'), ],

    )

    class Meta:
        model = models.PrettyNum
        fields = ['id', 'mobile', 'price', 'level', 'status']
        # fields = "__all__"  # 所有字段
        # exclude = ['level']  # 排除字段

    # # 验证手机号方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        if_exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if if_exists:
            raise ValidationError("手机号已存在！")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")

        return txt_mobile


class PrettyModelFormEdit(BootStrapModelForm):
    # 验证手机号格式方式1,disabled=True,表示mobile不可改
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机格式错误'), ],
        disabled=True,

    )

    class Meta:
        model = models.PrettyNum
        # fields = ['id', 'mobile', 'price', 'level', 'status']
        fields = "__all__"  # 所有字段
        # exclude = ['mobile']  # 排除字段

    # 验证手机号方式2
    def clean_mobile(self):

        # 根据主键获取id
        # self.instance.pk
        txt_mobile = self.cleaned_data['mobile']
        if_exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exclude(id=self.instance.pk).exists()
        if if_exists:
            raise ValidationError("手机号已存在！")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")

        return txt_mobile


class AdminModelForm(BootStrapModelForm):
    # widget=forms.PasswordInput(render_value=True)参数作用：假如密码不一致，保存原两个表单的数据
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        """密码加密"""
        pwd = self.cleaned_data.get('password')
        return md5(pwd)  # return值覆盖clean_data 中的值 同：clean_confirm_password

    # 钩子函数
    def clean_confirm_password(self):
        # return True if self.cleaned_data.get('password') == self.cleaned_data.get('confirm_password') else False

        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        # 对密文进行比较
        if confirm != pwd:
            # 失败，抛异常，会生成一个li标签加到form.py下form里的对象的errors属性中
            raise ValidationError("密码不一致")

        # return 的值会覆盖原表单用户输入的重复密码(clean_confirm_password)覆盖clean_后面的变量

        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username', ]


class AdminResetModelForm(BootStrapModelForm):
    # widget=forms.PasswordInput(render_value=True)参数作用：假如密码不一致，保存原两个表单的数据
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {'password': forms.PasswordInput(render_value=True)}

    def clean_password(self):
        """密码加密"""
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        # 校验新密码和老密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能和以前的密码一致")

        return md5_pwd  # return值覆盖clean_data 中的值 同：clean_confirm_password

    # 钩子函数
    def clean_confirm_password(self):
        # return True if self.cleaned_data.get('password') == self.cleaned_data.get('confirm_password') else False

        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        # 对密文进行比较
        if confirm != pwd:
            # 失败，抛异常，会生成一个li标签加到form.py下form里的对象的errors属性中
            raise ValidationError("密码不一致")

        # return 的值会覆盖原表单用户输入的重复密码(clean_confirm_password)覆盖clean_后面的变量
        return confirm


class LoginForm(BootstrapForm):
    """登录"""
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True,

    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            'detail': forms.TextInput
        }


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ['oid', 'admin']


class UploadForm(BootstrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


class UploadModalForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"
