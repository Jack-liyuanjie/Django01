from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user.models import UserModel
from rest_framework.decorators import api_view
from api.user import UserModelSerializer


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        error_msg = '用户名或口令出错'
        name = request.POST.get('name', None)
        password = request.POST.get('password', None)

        if all((name, password)):
            user_qs = UserModel.objects.filter(name=name)
            if user_qs.exists():
                user = user_qs.first()
                if check_password(password, user.auth_key):
                    request.session['login_user'] = {
                        'id': user.id,
                        'name': user.name
                    }

                    return redirect('/active/info/')
            else:
                error_msg = '用户名不存在请先注册'
        return render(request, 'login.html', locals())


# 通过类视图
class UserAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        datas = UserModel.objects.all()
        serializer = UserModelSerializer(datas, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserAPIDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,pk):
        datas = UserModel.objects.get(pk=pk)
        serializer = UserModelSerializer(datas)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        instance = UserModel.objects.get(pk=pk)
        serializer = UserModelSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        instance = UserModel.objects.get(pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def user_api(request):
    if request.method == 'GET':
        datas = UserModel.objects.all()
        serializer = UserModelSerializer(datas, many=True)

        return Response(serializer.data)
    else:
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_api_detail(request, pk):
    instance = UserModel.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserModelSerializer(instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        print(request.data)
        serializer = UserModelSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
