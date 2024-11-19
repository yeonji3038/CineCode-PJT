from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model


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