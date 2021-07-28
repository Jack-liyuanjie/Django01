import os
import random
from datetime import datetime

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Avg, Count, Max, Min, Sum,F,Q
from django.template import loader

from mainapp.models import UserEntity, FruitEntity, StoreEntity
from helloDjango.settings import BASE_DIR

# Create your views here.

def user_list(request):
    datas = [
        {'id': 101, 'name': '王大锤'},
        {'id': 102, 'name': '王二锤'},
        {'id': 103, 'name': '王小锤'},
    ]
    return render(request, 'user/list.html', {
        'users': datas,
        'msg': '最优秀学员',
    })


def user_list2(request):
    datas = [
        {'id': 101, 'name': '王大锤'},
        {'id': 102, 'name': '王二锤'},
        {'id': 103, 'name': '王小锤'},
    ]
    msg = '最优秀学员'
    return render(request, 'user/list.html', locals())


# --------------------------------------------------------------------------------------------------------------
def user_list3(request):
    users = UserEntity.objects.all()
    msg = '最优秀学员'
    error_index = random.randint(0,users.count()-1)
    vip = {
        'name': 'disen',
        'money': 20000
    }
    # # 加载模板
    # template = loader.get_template('user/list.html')
    #
    # # 渲染模板
    # html = template.render(context={
    #     'msg': msg,
    #     'users': users
    # })
    file_path = os.path.join(BASE_DIR,'mainapp/models.py')
    file_stat = os.stat(file_path)

    names = []

    file_dir = os.path.join(BASE_DIR,'mainapp/')
    files = {file_name: os.stat(file_dir+file_name)
             for file_name in os.listdir(file_dir)
             if os.path.isfile(file_dir+file_name)}

    now = datetime.now()

    price = 13.1356

    img_html= "<img width=200 height=200 src='/media/fruit/微信截图_20210715141106.png/'"

    info = '<p>我的简介</p><h1>我爱读书</h1><h2>我爱读python类的书</h2>'

    html = loader.render_to_string('user/list.html', locals())

    return HttpResponse(html, status=200)  # 如何增加响应头？？？


# 增
# 写一个脚本添加数据
def add_user(request):
    # 从GET请求中读取数据(从查询参数中)
    # request.GET.get('name')

    # request.GET 是一个字典类型，保存的是一个查询参数
    name = request.GET.get('name', None)
    age = request.GET.get('age', 0)
    phone = request.GET.get('phone', None)

    # 验证数据是否完整
    if not all((name, age, phone)):  # 有一个参数不存在则返回
        return HttpResponse('<h3 style="color:red">请求参数不完整</h3>', status=405)

    u1 = UserEntity()
    u1.name = name
    u1.age = age
    u1.phone = phone
    u1.save()
    return redirect('/user/list')


# 改
def update_user(request):
    # 查询参数id，name，phone
    # 通过模型查询id的用户是否存在
    id = request.GET.get('id', None)
    if not id:
        return HttpResponse('id参数必须提供', status=400)
    # Model类.objects.get()可能会出现异常报错--捕获异常
    try:
        u = UserEntity.objects.get(pk=int(id))
        name = request.GET.get('name', None)
        phone = request.GET.get('phone', None)
        if any((name, phone)):  # name或者phone 任意一个存在即可
            if name:
                u.name = name
            if phone:
                u.phone = phone

            # u.name = '李元霸'
            # u.age = 17
            # u.phone = 120
            u.save()
        return redirect('/user/list')
    except:
        return HttpResponse('<h3 style="color:red">查无此人</h3>')


# 删除
def delete_user(request):
    # 查询参数有id
    # 验证id是否存在
    id = request.GET.get('id', None)
    if not id:
        return HttpResponse('id参数必须提供', status=400)
    try:
        u = UserEntity.objects.get(pk=int(id))
        u.delete()
        html = """
        <p>
        %s 删除成功！ 三秒后自动跳转到<a href="/user/list">列表</a>
        </p>
        <script>
            setTimeout(function(){
            open('/user/list', target='_self');
            },3000)
        </script>
        """ % id
        return HttpResponse(html)
    except:
        return HttpResponse('<h3 style="color:red">查无此人</h3>')


def find_fruit(request):
    # 从查询参数中获取价格区间price1，price2
    price1 = request.GET.get('price1', 0)
    price2 = request.GET.get('price2', 1000)

    # 根据价格区间查找所有的满足条件的水果信息
    fruits = FruitEntity.objects.filter(price__gte=price1,
                                        price__lte=price2) \
        .exclude(price=250).filter(name__contains='果').all()

    # 将查询到的数据渲染到html模板中
    return render(request, 'fruit/list.html', locals())


def find_store(request):
    # 查询大于17小于19年年开业的水果店
    # 查询参数: year
    # stores = StoreEntity.objects.filter(create_time__year__gt=2017,create_time__year__lt=2019).all()
    stores = StoreEntity.objects.filter(create_time__year__lt=2019).order_by(-'create_time').all()
    queryset = stores.first()
    return render(request, 'store/list.html', locals())


# value返回json数据
def all_store(request):
    # 返回所有水果店的json数据
    result = {}
    if StoreEntity.objects.exists():
        datas = StoreEntity.objects.values()
        print(type(datas))

        store_list = []
        for store in datas:
            store_list.append(store)

        result['data'] = store_list
        result['total'] = StoreEntity.objects.count()

    else:
        result['msg'] = '数据是空的'

    return JsonResponse(result)


def count_fruit(request):
    # 返回json数据：统计每种分类的水果数据，最高价格，和最低价格和总价格
    result = FruitEntity.objects.aggregate(Count('name'),Min('price'),Max('price'),Avg('price'),Sum('price'))

    # 中秋节：全场水果打8.8折 F条件
    FruitEntity.objects.update(price=F('price')*0.88)
    fruits = FruitEntity.objects.values() # 返回的是QuerySet对象

    # 查询价格低于10，或者高于100的水果,或者是原产地广州而且名字带果的
    fruit2 = FruitEntity.objects.filter(
        Q(price__lte=10) | Q(price__gte=100) | Q(Q(name__contains='果') & Q(source='广州'))).values()
    return JsonResponse({
        'count': result,
        'fruits': [fruit for fruit in fruits],
        'multi_query':[fruit for fruit in fruit2]
    })