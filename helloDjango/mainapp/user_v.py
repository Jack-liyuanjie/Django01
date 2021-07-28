from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

from mainapp.models import UserEntity


# @csrf_exempt
def login(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)

        # 验证用户名和密码是否为空
        if not all((name,password)):
            error_msg = '用户名和密码不能为空'
        else:
            # 验证用户是否存在
            qs = UserEntity.objects.filter(name=name)
            if qs.exists():
                login_user: UserEntity = qs.first()
                print(qs.first()) # 李元杰
                if check_password(password, login_user.password):
                    # 登陆成功
                    # 将用户信息写入到session中
                    request.session['login_user'] = {
                        'name': login_user.name,
                        'user_age': login_user.age,
                        'user_p': login_user.phone
                    }
                    return redirect('/user/list')
            else:
                error_msg = '用户名未注册，<a href=/user/regist>去注册</a>'
    return render(request, 'user/login.html',locals())
