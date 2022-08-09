"""物协网站 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web.views import index

urlpatterns = [
    path('index/', index.index),
    path('index/association/', index.association),
    path("index/register/", index.register),
    path("admin/login/", index.admin_login),
    path('image/code/', index.image_code),
    path('admin/index/', index.admin_index),
    path('admin/add/student/', index.admin_add_student),
    path('student/<int:nid>/edit/', index.edit),
    path('student/<int:nid>/data/', index.data),
    path("admin/add/", index.admin_add),
    path("logout/", index.admin_logout),
    path("student/login/", index.student_login),
    path("student/index/", index.student_index),
    path("student/logout/", index.student_logout),
    path("stud/<int:nid>/edit/", index.stud_exit),
    path("development/planning/", index.development_planning),
    path("study/planning/", index.study_planning),
    path("study/c/", index.study_c),
    path("study/python/", index.study_python),
    path("study/web/",index.study_web),
    path("study/java/",index.study_java),
]
