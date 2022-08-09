from web import models
from django import forms
import hashlib
from django.conf import settings
from django.core.exceptions import ValidationError


# 定义MD5
def md5(string):
    hash_object = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    hash_object.update(string.encode('utf-8'))
    return hash_object.hexdigest()


# 定义bootstrap类
class BootStrapModelForm(forms.ModelForm):
    bootstrap_class_exclude = []

    # 定义init方法
    def __init__(self, *args, **kwargs):
        # 执行父类的init方法
        super().__init__(*args, **kwargs)

        # 循环modelform每一个字段，设置字段的插件
        for name, field in self.fields.items():
            if name in self.bootstrap_class_exclude:
                continue
            if field.widget.attrs:
                # 若字典内有值
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = "请输入{}".format(field.label)
            else:
                # 若字典内有值
                field.widget.attrs = {"class": "form-control"}


# 定义注册类
class RegisterModelForm(BootStrapModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}),
                               label="密码", max_length=16,
                               min_length=8, error_messages={'min_length': "密码长度不能小于8位", 'max_length': "密码长度不能超过16位"})
    confine_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={"placeholder": "请确认密码"}))

    class Meta:
        model = models.StudentInfo
        fields = ["username", "gender", "student_number", "password", "confine_password", "student_qq",
                  "mobile_phone"]

    # 定义钩子用户名
    def clean_username(self):
        username = self.cleaned_data["username"]
        exists = models.StudentInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return username

    # 定义学号的钩子
    def clean_student_number(self):
        student_number = self.cleaned_data["student_number"]
        if not student_number:
            raise ValidationError("学号不能为空")
        exists = models.StudentInfo.objects.filter(student_number=student_number).exists()
        if exists:
            raise ValidationError("学号已存在")
        return student_number

    # 定义密码钩子
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)

    # 定义验证密码和密码相同的钩子
    def clean_confine_password(self):
        pwd = self.cleaned_data["password"]
        confirm_pwd = self.cleaned_data["confine_password"]
        if pwd != md5(confirm_pwd):
            return ValidationError("密码与验证码不同，请重新输入")
        return confirm_pwd

    # 定义验证手机号的钩子
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data["mobile_phone"]
        exists = models.StudentInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return mobile_phone

    # 定义qq的钩子
    def clean_student_qq(self):
        student_qq = self.cleaned_data["student_qq"]
        exists = models.StudentInfo.objects.filter(student_qq=student_qq).exists()
        if exists:
            raise ValidationError("QQ已存在")
        return student_qq


# 定义管理员登录
class AdminLogin(BootStrapModelForm):
    admin_number = forms.CharField(label="学号", widget=forms.TextInput(attrs={"placeholder": "请输入学号"}))
    admin_password = forms.CharField(label="密码",
                                     widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}, render_value=True))
    code = forms.CharField(label="图片验证码", widget=forms.TextInput(attrs={"placeholder": "请输入图片验证码"}))

    class Meta:
        model = models.Admin
        fields = ['admin_number', 'admin_password', 'code']

    # 重写init方法
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # 定义密码的钩子
    def clean_admin_password(self):
        admin_password = self.cleaned_data["admin_password"]
        return md5(admin_password)

    # 定义图片验证码的钩子
    def clean_code(self):
        code = self.cleaned_data["code"]
        # 去session中获取验证码
        session_code = self.request.session.get('image_code')
        if not code.upper().strip() == session_code:
            raise ValidationError("验证码输入错误")
        return code


# 管理员注册成员form
class AdminAddStudent(BootStrapModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}),
                               label="密码", max_length=16,
                               min_length=8, error_messages={'min_length': "密码长度不能小于8位", 'max_length': "密码长度不能超过16位"})
    confine_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={"placeholder": "请确认密码"}))

    class Meta:
        model = models.StudentInfo
        fields = ["username", "gender", "student_number", "password", "confine_password", "student_qq",
                  "mobile_phone"]

    # 定义钩子用户名
    def clean_username(self):
        username = self.cleaned_data["username"]
        exists = models.StudentInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return username

    # 定义学号的钩子
    def clean_student_number(self):
        student_number = self.cleaned_data["student_number"]
        if not student_number:
            raise ValidationError("学号不能为空")
        exists = models.StudentInfo.objects.filter(student_number=student_number).exists()
        if exists:
            raise ValidationError("学号已存在")
        return student_number

    # 定义密码钩子
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)

    # 定义验证密码和密码相同的钩子
    def clean_confine_password(self):
        pwd = self.cleaned_data["password"]
        confirm_pwd = self.cleaned_data["confine_password"]
        if pwd != md5(confirm_pwd):
            return ValidationError("密码与验证码不同，请重新输入")
        return confirm_pwd

    # 定义验证手机号的钩子
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data["mobile_phone"]
        exists = models.StudentInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return mobile_phone

    # 定义qq的钩子
    def clean_student_qq(self):
        student_qq = self.cleaned_data["student_qq"]
        exists = models.StudentInfo.objects.filter(student_qq=student_qq).exists()
        if exists:
            raise ValidationError("QQ已存在")
        return student_qq


# 定义修改类
class AdminExitStudent(BootStrapModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}), label="密码")
    confine_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={"placeholder": "请确认密码"}))

    class Meta:
        model = models.StudentInfo
        fields = ["username", "gender", "student_number", "password", "confine_password", "student_qq",
                  "mobile_phone"]

    # 定义密码钩子
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        if len(pwd) > 18 or len(pwd) < 8:
            raise ValidationError("密码的长度必须小于18位且大于8位")
        return md5(pwd)

    # 定义验证密码和密码相同的钩子
    def clean_confine_password(self):
        pwd = self.cleaned_data.get("password")
        confirm_pwd = self.cleaned_data["confine_password"]
        if pwd != md5(confirm_pwd):
            raise ValidationError("密码与验证码不同，请重新输入")
        return confirm_pwd


# 定义管理员注册类
class AdminAdd(BootStrapModelForm):
    admin_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}),
                                     label="密码", max_length=16,
                                     min_length=8,
                                     error_messages={'min_length': "密码长度不能小于8位", 'max_length': "密码长度不能超过16位"})
    confine_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={"placeholder": "请确认密码"}))

    class Meta:
        model = models.Admin
        fields = ["admin_name", "admin_number", "admin_password", "confine_password"]

    def clean_admin_name(self):
        admin_name = self.cleaned_data["admin_name"]
        exists = models.Admin.objects.filter(admin_name=admin_name).exists()
        if exists:
            raise ValidationError("学号已存在")
        return admin_name

    def clean_admin_password(self):
        admin_password = self.cleaned_data["admin_password"]
        if len(admin_password) > 16 or len(admin_password) < 8:
            raise ValidationError("密码的长度必须大于8位且小于16位")
        return md5(admin_password)

    def clean_confine_password(self):
        confine_password = self.cleaned_data["confine_password"]
        admin_password = self.cleaned_data.get("admin_password")
        if md5(confine_password) != admin_password:
            raise ValidationError("密码和验证码不一致")
        return confine_password


class StudentLogin(BootStrapModelForm):
    student_number = forms.CharField(label="学号", widget=forms.TextInput(attrs={"placeholder": "请输入学号"}))
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={"placeholder": "请输入密码"}, render_value=True))
    code = forms.CharField(label="图片验证码", widget=forms.TextInput(attrs={"placeholder": "请输入图片验证码"}))

    class Meta:
        model = models.StudentInfo
        fields = ['student_number', 'password', 'code']

    # 重写init方法
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    # 定义密码的钩子
    def clean_password(self):
        password = self.cleaned_data["password"]
        return md5(password)

    # 定义图片验证码的钩子
    def clean_code(self):
        code = self.cleaned_data["code"]
        # 去session中获取验证码
        session_code = self.request.session.get('image_code')
        if not code.upper().strip() == session_code:
            raise ValidationError("验证码输入错误")
        return code
