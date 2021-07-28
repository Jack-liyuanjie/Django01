import json
import os
import random
import string
import uuid

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.uploadhandler import InMemoryUploadedFile
from django.core.paginator import Paginator
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageDraw, ImageFont
from django.db.models import Q

import signals
from common.code import new_code_str
from user.models import Order
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@csrf_exempt
def regist_2(request, user_id=None):
    loves = ['python', 'java', 'H5', 'PHP']
    # 获取参数名相同的多个参数值
    select_loves = [request.GET.getlist('love')]
    return render(request, 'regist2.html', locals())


@csrf_exempt
def regist3(request, user_id=None):
    # print(request.body)
    # print(request.POST)  # 只接收post请求上传的表单数据
    # print(request.method)
    # print(request.FILES)

    # 表单数据获取
    name = request.POST.get('name')
    phone = request.POST.get('phone')

    upload_file: InMemoryUploadedFile = request.FILES.get('img1')
    if upload_file:
        # print(upload_file.name)  # 文件名
        # print(upload_file.content_type)  # 文件类型 MIMETYPE image/png;
        # print(upload_file.size)  # 文件大小
        # print(upload_file.charset)

        # 文件过滤要求上传必须是图片而且小于50k
        if all((
                upload_file.content_type.startswith('image/'),
                upload_file.size < 1000 * 1024
        )):
            print(request.META.get('REMOTE_ADDR'), '上传了', upload_file)
            filename = name + os.path.splitext(upload_file.name)[-1]

            # 将内存中文件写入磁盘中
            with open('images/' + filename, 'wb') as f:
                # 分段写入
                for chunk in upload_file.chunks():
                    f.write(chunk)
                f.flush()
            return HttpResponse('上传文件成功')
        else:
            return HttpResponse('请上传小于50k的图片')
    # # 查看META元信息
    # print(request.META)

    return render(request, 'regist4.html', locals())


@csrf_exempt
def regist(request):
    resp1 = HttpResponse(content='您好'.encode('utf-8'),
                         status=200,
                         content_type='text/html;charset=utf-8')

    with open('images/李元杰.png', 'rb') as f:
        bytes = f.read()

    # 响应图片数据
    resp2 = HttpResponse(content=bytes,

                         content_type='image/png')
    # ?? 响应头如何设设置

    # 响应json数据
    data = {'name': 'disen', 'age': 20}
    # 序列化是把字典转成字符串，反序列化是把字符串转成字典
    # json.dumps()序列化  json.loads()反序列化
    resp3 = HttpResponse(content=json.dumps(data),
                         content_type='application/json')

    resp4 = JsonResponse(data)  # 直接使用JsonResponse响应数据
    return resp4


def add_cookie(request):
    # 生成token，并存储到Cookie中
    token = uuid.uuid4().hex

    resp = HttpResponse('增加Cookie： token成功')

    from datetime import datetime, timedelta
    resp.set_cookie('token', token, expires=datetime.now() + timedelta(minutes=2))

    return resp


def del_cookie(request):
    resp = HttpResponse('删除Cookie：token成功!')
    # 删除单个cookie
    # resp.delete_cookie('token')

    # 删除所有cookie
    # 先从请求对象中获取所有的Cookie信息在删除
    for k in request.COOKIES:
        resp.delete_cookie(k)
    return resp


def login(request):
    phone = request.GET.get('phone')
    code = request.GET.get('code')

    # 判断缓存中是否存在phone
    # 存在则读取
    if all((
            cache.has_key(phone),
            cache.get(phone) == code
    )):
        resp = HttpResponse('登陆成功')
        token = uuid.uuid4().hex  # 保存到缓存中
        resp.set_cookie('token', token)

        # 删除缓存
        cache.delete(phone)

        return resp

    return HttpResponse('登陆失败，请确认phone和code!')


def logout(request):
    # 删除所session中的信息和cookie信息
    # request.session.clear() # 删除所有session中的信息
    request.session.flush()
    resp = HttpResponse('注销成功')
    resp.delete_cookie('token')
    return resp


# @cache_page(timeout=10, cache='html', key_prefix='page')
def list(request):
    # 验证是否登录
    # if request.COOKIES.get('token'):
    #     return HttpResponse('正在跳转到主页')
    chrs = string.ascii_letters
    num = random.choice(chrs)
    return HttpResponse('用户列表页面:<br> %s' % num)


def new_code(request):
    # 生成手机验证码
    # 随机产生验证码：大小写字母+数字

    # all_char = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    # index = len(all_char) + 1
    # code = ''
    # for i in range(4):
    #     code_txt = random.randint(0, index)
    #     code += all_char[code_txt]
    from common import code
    code = code.new_code_str(4)

    phone = request.GET.get('phone', '')

    # 发送信号
    # sender 名字跨域根据需求设定
    # 关键参数列表，根据信号定义的参数列表传值
    signals.codeSignal.send('new_code',
                            path=request.path,
                            phone=phone,
                            code=code)

    # 保存到session中,session信息存在mysql中
    request.session['code'] = code
    request.session['phone'] = phone

    # 将验证码存到cache
    # timeout是缓存的时间
    cache.set(phone, code,timeout=60)

    # 向手机发送验证码：华为云：短信服务
    return HttpResponse('已经向%s手机发送了验证码！验证码为:%s' % (phone, code))


def new_img_code(request):
    # 创建一个画布
    img = Image.new('RGB', (120, 40), (100, 100, 0))

    # 从画布中获取画笔
    draw = ImageDraw.Draw(img, 'RGB')

    # 创建字体对象和字体颜色
    font_color = (0, 20, 100)
    font = ImageFont.truetype(font='static/fonts/YuGothB.ttc', size=20)

    # 通过自写脚本生成验证码
    valid_code = new_code_str(6)
    request.session['code'] = valid_code
    # 开始画内容
    draw.text((5, 5), valid_code, font=font, fill=font_color)
    # draw.line((0,0),(255,0,0),20)

    for _ in range(100):
        x = random.randint(0, 120)
        y = random.randint(0, 40)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        draw.point((x, y), (r, g, b))

    # 将画布写入内存字节数组中
    from io import BytesIO
    buffer = BytesIO()
    img.save(buffer, 'png')  # 写入

    return HttpResponse(content=buffer.getvalue(),
                        content_type='image/png')


def order_list(request):
    wd = request.GET.get('wd', '')
    page = request.GET.get('page', 1)
    orders = Order.objects.filter(Q(title__icontains=wd)).all()

    # 分页器Paginator
    paginator = Paginator(orders, 3)
    pager = paginator.page(page)  # 查询第几页
    return render(request, 'list.html', locals())
