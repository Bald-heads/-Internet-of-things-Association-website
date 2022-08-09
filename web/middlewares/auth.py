from django.utils.deprecation import MiddlewareMixin
from web import models
from django.conf import settings
from django.shortcuts import redirect


# 定义中间件
class AutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        nid = request.session.get("admin_id")
        admin_object = models.Admin.objects.filter(id=nid).first()
        if admin_object:
            request.tracer = admin_object
        else:
            nid = request.session.get("student_id", 0)
            student_object = models.StudentInfo.objects.filter(id=nid).first()
            request.tracer_student = student_object
        info_admin_dict = request.session.get("admin_id")
        info_student_dict = request.session.get("student_id")
        if request.path_info in settings.WHITE_REGEX_LIST:
            return
        if not info_admin_dict:
            if not info_student_dict:
                return redirect("/student/login/")
