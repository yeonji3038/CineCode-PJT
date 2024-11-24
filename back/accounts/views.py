from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import UserUpdateSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .serializers import UserProfileSerializer


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


# 프로필
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
    }
    return Response(data)



# 회원가입 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    
    # 이메일 업데이트
    if 'email' in request.data:
        user.email = request.data['email']
    
    # 비밀번호 업데이트
    if 'password1' in request.data and 'password2' in request.data:
        if request.data['password1'] == request.data['password2']:
            user.set_password(request.data['password1'])
        else:
            return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 프로필 이미지 업데이트
    if 'profile_image' in request.FILES:
        user.profile_image = request.FILES['profile_image']
    
    user.save()
    
    return Response({
        'email': user.email,
        'message': '회원정보가 성공적으로 업데이트되었습니다.'
    })

# #소셜 로그인
PASSWORD = getattr(settings, "DEFAULT_USER_PASSWORD", "default_password")

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
        ).save()
        user = get_user_model().objects.get(username = id)
        user.set_password(PASSWORD)
        user.save()
        data = {
            "username" : user.username
        }
        
        return Response(data, status.HTTP_200_OK)
    
# @api_view(['GET', 'POST'])
# def get_naver_info(request):
#     token = request.data['token']
#     header = "Bearer " + token # Bearer 다음에 공백 추가
#     url = "https://openapi.naver.com/v1/nid/me"
#     request = urllib.request.Request(url)
#     request.add_header("Authorization", header)
#     response = urllib.request.urlopen(request)
#     rescode = response.getcode()
#     if(rescode==200):

#         response_body = response.read()
#         res_data = json.loads(response_body.decode('UTF-8'))
#         id = res_data['response']['id']
#         nickname = res_data['response']['nickname']

#         # 응답 성공했을 때 유저 있는 지 확인, 있다면 기존 아이디를 돌려줌
#         if get_user_model().objects.filter(username=id).exists():
#             user = get_user_model().objects.get(username = id)
#             data = {
#             "username" : user.username
#             }
#             return Response(data, status.HTTP_200_OK)
#         # 없다면 회원가입 시킨 후 돌려줌 
#         else: 
#             get_user_model()(
#             username = id,
#             nickname = nickname,
#             ).save()
#             user = get_user_model().objects.get(username = id)
#             user.set_password(PASSWORD)
#             user.save()
#             data = {
#                 "username" : user.username
#             }
#             return Response(data, status.HTTP_200_OK)
#     else:
#         print("Error Code:" + rescode)
#         return Response(status.HTTP_400_BAD_REQUEST)
class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    
    def get_object(self):
        return self.request.user
    
class UserProfileView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
