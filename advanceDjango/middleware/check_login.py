# --coding:utf-8--
import logging

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

from stockapp.views import ContextError


class CheckLoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = request.get_raw_uri()
        msg = "%s 访问 %s" % (ip,path)
        logging.getLogger('mylogger').error(msg)
        # 从请求到路由urls过程，触发此函数
        # print('--CheckLoginMiddleware--', 'process_request')
        # print(request.path,
        #       request.COOKIES)

        # 验证用户是否登录
        dontfilters = ['/user/login/','/user/code/']
        if request.path not in dontfilters:
            if not request.COOKIES.get('token'):
                return HttpResponse('请登录')

    def process_view(self, request,callback,callback_args,callback_kwargs):
        # print('--CheckLoginMiddleware--', 'process_view')
        # callback 时调用的view函数
        # 新增一个关键参数，类似与匹配路由stock/<stock_id>/<page>/
        # callback_kwargs['page'] = request.GET.get('page',1)
        print(callback,callback_args,callback_kwargs)

    def process_exception(self,request,exception):
        # print('--CheckLoginMiddleware--','process_exception')
        # print(exception,type(exception))
        if isinstance(exception,ContextError):
            return HttpResponse('Context中处理中出现异常:%s' % exception)
        else:
            return HttpResponse('登录的过程中出现异常：%s' % exception)

    def process_response(self, request, response):
        # print('--CheckLoginMiddleware--', 'process_response')
        return response