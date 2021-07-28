# --coding:utf-8--
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponse


class CachePageMiddleware(MiddlewareMixin):
    # 配置缓存的页面路径
    cache_page_path = [
        '/user/list/'
    ]

    def process_request(self, request):
        # 判断当前的请求是否支持缓存
        if request.path in self.cache_page_path:
            # 判断页面是否已经缓存了
            if cache.has_key(request.path):
                return HttpResponse(cache.get(request.path))

    def process_response(self, request, response):
        # 判断当前的请求路径是否要被缓存
        if request.path in self.cache_page_path:
            # 开始缓存
            cache.set(request.path,
                      response.content, timeout=5)

        return response
