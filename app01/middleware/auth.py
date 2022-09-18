from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    """中间件"""

    def process_request(self, request):

        # 0.排除那些不需要登录就能访问的页面
        #   request.path_info 获取当前用户请求的URL /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1、读取当前访问的用户的session信息。如果能读到，说明已经登陆过，继续走
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 2、没登陆过
        return redirect('/login/')
