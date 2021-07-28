from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from actives.models import ActiveModel
from .tasks import qbuy_task

import libs.cache as libs_cache


class ActiveGoodsView(TemplateView):
    template_name = 'goods_list.html'

    def get_context_data(self, **kwargs):
        context = super(ActiveGoodsView, self).get_context_data(**kwargs)

        active = ActiveModel.objects.get(pk=1)
        context['active'] = active

        return context


def qbuy_api(request,goods_id):
    # 验证当前用户是否已登录
    login_user = request.session.get('login_user', None)
    if not login_user:
        return JsonResponse({
            'code':100,
            'msg': '当前用户未登录'
        })

    # login_user = {'id':11,'name':'disen'}
    user_id = login_user.get('id')
    qbuy_task.delay(user_id,goods_id)

    return JsonResponse({
        'code':201,
        'msg': '抢购中'
    })


def query_qbuy_api(request,goods_id):
    login_user = request.session.get('login_user', None)
    if not login_user:
        return JsonResponse({
            'code': 100,
            'msg': '当前用户未登录'
        })

    user_id = login_user.get('id')
    if libs_cache.exist_qbuy(user_id):
        qbuy_goods_id = libs_cache.get_qbuy(user_id)

        if goods_id == qbuy_goods_id:
            return JsonResponse({
                'code':200,
                'msg':'抢购成功'
            })
        else:
            return JsonResponse({
                'code':202,
                'msg':'每天只限一次抢购'
            })
    elif libs_cache.is_qbuyable():
        return JsonResponse({
            'code':201,
            'msg':'抢购中'
        })
    else:
        return JsonResponse({
            'code':300,
            'msg':'抢购失败'
        })

