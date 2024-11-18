from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, SignupSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    password = request.data.get('password')
    if serializer.is_valid(raise_exception=True):
        # 비밀번호 해싱
        if serializer.validated_data.get('password') == serializer.validated_data.get('password2'):
            user = serializer.save()
            # print(user)
            user.set_password(password)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    pass