from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def order_list(request, order_num, city_code):
    print(order_num, city_code)
    return render(request, 'list_order.html', locals())


def cancel_order(request, order_num):
    # order_num订单编号是UUID类型的
    print(order_num)
    return render(request, 'list_order.html', locals())


def search_p(request, phone):
    return HttpResponse(phone)


def query(request):
    # 查询参数中code(1：按城市city和订单号num查询
    #              2：按手机号phone查询)
    # url = reverse('order:search', args=('17791306788',))
    # return redirect(url)
    # return HttpResponse('hi,query %s' % url)
    url = reverse('order:list', kwargs=dict(city_code='shanghai',order_num='11425'))
    # return redirect(url)
    return HttpResponseRedirect(url)