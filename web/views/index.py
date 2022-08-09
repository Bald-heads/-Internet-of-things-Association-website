from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from web.forms.login import RegisterModelForm, AdminLogin, AdminAddStudent, AdminExitStudent, AdminAdd, StudentLogin
from web import models
from django.utils.safestring import mark_safe


# 官网
def index(request):
    return render(request, "index.html")


# 新生注册
def association(request):
    return render(request, 'index.html')


# 注册
def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {"forms": form})
    elif request.method == "POST":
        form = RegisterModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": True, 'data': '/student/login/'})
        return JsonResponse({'status': False, 'error': form.errors})


# 管理员登录类
def admin_login(request):
    if request.method == "GET":
        form = AdminLogin(request)
        return render(request, 'admin_login.html', {"form": form})
    form = AdminLogin(request, data=request.POST)
    if form.is_valid():
        admin_number = form.cleaned_data["admin_number"]
        password = form.cleaned_data.get("admin_password")
        user_object = models.Admin.objects.filter(admin_number=admin_number, admin_password=password).first()
        if user_object:
            # 写入session中
            request.session['admin_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 7)
            request.num = 1
            return redirect('/admin/index/')
        form.add_error('admin_number', '学号或密码错误')
    return render(request, 'admin_login.html', {'form': form})


# 生成图片验证码
def image_code(request):
    from io import BytesIO
    from web.utils.image_code import check_code
    image_object, code = check_code()
    request.session["image_code"] = code
    # 主动修改session过期事件
    request.session.set_expiry(60)
    # 把图片写到内存中
    stream = BytesIO()
    image_object.save(stream, 'png')
    stream.getvalue()
    return HttpResponse(stream.getvalue())


# 管理员页面
def admin_index(request):
    plus = 2
    value = request.GET.get("q")
    page = int(request.GET.get('page', 1))
    start_page = page - plus
    if start_page < 0 or start_page == 0:
        start_page = 1
    end_page = page + plus
    page_size = 10
    start = (page - 1) * 10
    end = page * 10
    page_str_list = []
    if value:
        obj = models.StudentInfo.objects.filter(username__contains=value)[start:end]
        return render(request, 'admin_index.html', {'objects': obj})
    obj = models.StudentInfo.objects.filter()[start:end]
    total_count = models.StudentInfo.objects.all().count()
    total_count_page, div = divmod(total_count, page_size)
    if div:
        total_count_page += 1
    # 首页：
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    # 下一页
    if page < total_count_page:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(total_count_page)
    page_str_list.append(prev)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_count_page))
    page_string = mark_safe("".join(page_str_list))
    return render(request, 'admin_index.html', {'objects': obj, 'page_string': page_string})


# 管理员注册成员页面
def admin_add_student(request):
    if request.method == "GET":
        form = AdminAddStudent()
        return render(request, "admin_add_student.html", {"forms": form})
    elif request.method == "POST":
        form = AdminAddStudent(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin/index/")
        return render(request, 'admin_add_student.html', {"forms": form})


# 编辑成员信息
def edit(request, nid):
    row_object = models.StudentInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminExitStudent(instance=row_object)
        return render(request, 'user_edit.html', {"forms": form})
    elif request.method == "POST":
        form = AdminExitStudent(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            # 重定向回主页面
            return redirect('/admin/index/')
        return render(request, 'user_edit.html', {"forms": form})


# 删除成员信息
def data(request, nid):
    models.StudentInfo.objects.filter(id=nid).delete()
    return redirect('/admin/index/')


# 添加管理员
def admin_add(request):
    if request.method == "GET":
        form = AdminAdd()
        return render(request, "admin_add.html", {"forms": form})
    elif request.method == "POST":
        form = AdminAdd(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin/index/")
        return render(request, 'admin_add_student.html', {"forms": form})


# 管理员退出登录
def admin_logout(request):
    request.session.flush()
    return redirect('/index/')


# 成员登录
def student_login(request):
    if request.method == "GET":
        form = StudentLogin(request)
        return render(request, 'student_login.html', {"form": form})
    form = StudentLogin(request, data=request.POST)
    if form.is_valid():
        student_number = form.cleaned_data["student_number"]
        password = form.cleaned_data.get("password")
        user_object = models.StudentInfo.objects.filter(student_number=student_number, password=password).first()
        if user_object:
            # 写入session中
            request.session['student_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 7)
            request.num = 2
            return redirect('/student/index/')
        form.add_error('student_number', '学号或密码错误')
    return render(request, 'student_login.html', {'form': form})


# 学生端主页
def student_index(request):
    if request.method == "GET":
        student_id = request.session.get("student_id")
        obj = models.StudentInfo.objects.filter(id=student_id)
        return render(request, 'student_index.html', {"objects": obj})


# 学生退出登录
def student_logout(request):
    request.session.flush()
    return redirect('/index/')


# 学生编辑自己信息
def stud_exit(request, nid):
    row_object = models.StudentInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminExitStudent(instance=row_object)
        return render(request, 'stud_exit.html', {"forms": form})
    elif request.method == "POST":
        form = AdminExitStudent(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            # 重定向回主页面
            return redirect('/student/index/')
        return render(request, 'stud_exit.html', {"forms": form})


# 发转规划
def development_planning(request):
    return render(request, 'development_planning.html')


# 学习方向
def study_planning(request):
    return render(request, 'choice.html')


def study_c(request):
    return render(request, "c.html")


def study_python(request):
    return render(request, "python.html")


def study_web(request):
    return render(request, "web.html")


def study_java(request):
    return render(request, "java.html")
