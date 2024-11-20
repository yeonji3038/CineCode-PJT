from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.contrib.auth.models import User
import urllib.request as url_request
import json
from django.contrib.auth import get_user_model
from django.conf import settings
import urllib.request

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'GET':
        return Response({"message": "Signup endpoint. Please use POST to register."}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data.get('password') == serializer.validated_data.get('password2'):
                user = serializer.save()
                user.set_password(user.password)  # 비밀번호를 해싱하여 저장
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        return Response({"message": "DELETE method is not implemented yet."}, status=status.HTTP_501_NOT_IMPLEMENTED)
    

@api_view(['POST'])
def login(request):
    pass

@api_view(['POST'])
def google(request):
    id = request.data['id']
    
    if get_user_model().objects.filter(username=id).exists():
        user = get_user_model().objects.get(username = id)
        data = {
            "username" : user.username
        }
        return Response(data, status.HTTP_200_OK)
    else:
        get_user_model()(
            username = id,
            nickname = id,
        ).save()
        user = get_user_model().objects.get(username = id)
        user.set_password(PASSWORD)
        user.save()
        data = {
            "username" : user.username
        }
        
        return Response(data, status.HTTP_200_OK)
    
PASSWORD = getattr(settings, "DEFAULT_USER_PASSWORD", "default_password")   
@api_view(['GET', 'POST'])
def get_naver_info(request):
    token = request.data['token']
    header = "Bearer " + token # Bearer 다음에 공백 추가
    url = "https://openapi.naver.com/v1/nid/me"
    request = urllib.request.Request(url)
    request.add_header("Authorization", header)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):

        response_body = response.read()
        res_data = json.loads(response_body.decode('UTF-8'))
        id = res_data['response']['id']
        nickname = res_data['response']['nickname']

        # 응답 성공했을 때 유저 있는 지 확인, 있다면 기존 아이디를 돌려줌
        if get_user_model().objects.filter(username=id).exists():
            user = get_user_model().objects.get(username = id)
            data = {
            "username" : user.username
            }
            return Response(data, status.HTTP_200_OK)
        # 없다면 회원가입 시킨 후 돌려줌 
        else: 
            get_user_model()(
            username = id,
            nickname = nickname,
            ).save()
            user = get_user_model().objects.get(username = id)
            user.set_password(PASSWORD)
            user.save()
            data = {
                "username" : user.username
            }
            return Response(data, status.HTTP_200_OK)
    else:
        print("Error Code:" + rescode)
        return Response(status.HTTP_400_BAD_REQUEST)