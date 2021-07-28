from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView,RedirectView

# Create your views here.


class StockView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self, request, **kwargs):
        stock_id = kwargs.get('stock_id')
        page = kwargs.get('page',5)
        return render(request, 'stock/list.html', locals())

    def post(self, request):
        return HttpResponse('Post请求')

    def put(self, request):
        return HttpResponse('put请求')

    def delete(self, request):
        return HttpResponse('delet请求')


# 分发方法以下方法已过时
# @csrf_exempt
# def goods(request):
#     method = request.method
#     handler = goods_get if method == "GET" else goods_post
#     return handler(request)
#
#
# def goods_get(request):
#     return render(request, 'stock/list.html', locals())
#
#
# def goods_post(request):
#     return HttpResponse('Post请求')

class LoginError(Exception):
    pass


class ContextError(Exception):
    pass


class GoodsView(TemplateView):
    template_name = 'goods/list.html'

    extra_context = {'msg': '我是扩展的消息'}

    def get_context_data(self, **kwargs):
        # 抛出异常
        # raise ContextError('抛出异常')
        # 渲染模板之前，提供上下文数据
        context = super(GoodsView, self).get_context_data(**kwargs)
        wd = context.get('wd','')

        datas = ['iphone 6','iphone 8', 'iphone x'] if wd == 'iphone'\
            else ['Vivo','huawei']

        context['datas'] = datas
        context['msg'] = '查询成功%s' % (datetime.now())
        return context


class QueryView(RedirectView):
    # 重定向的视图函数名
    pattern_name = 'stockapp:goods'

    # 需要拼接参数的话
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        # raise LoginError('测试查询异常')
        return super(QueryView, self).get_redirect_url(*args,**kwargs)
