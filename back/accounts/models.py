from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from rest_framework.exceptions import ValidationError

# User 모델: 사용자의 기본 정보를 저장하는 모델입니다.
class User(AbstractUser):
    nickname = models.CharField(max_length=150)  # 닉네임
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # 프로필 이미지
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    points = models.PositiveIntegerField(default=0)  # 기본 포인트 (0으로 초기화)
    payment_info = models.JSONField(null=True, blank=True)  # 결제 정보 (JSON 형태로 저장)

    def __str__(self):
        return self.username  # 사용자 이름을 반환



# Admin 모델: 관리자 계정 정보를 저장합니다.
class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)  # 관리자 이름
    password = models.CharField(max_length=128)  # 관리자 비밀번호
    permissions = models.JSONField()  # 관리자 권한 정보 (JSON 형태로 저장)
    created_at = models.DateTimeField(auto_now_add=True)  # 계정 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 계정 수정 시간 (자동으로 현재 시간으로 설정)

    def __str__(self):
        return self.username  # 관리자 이름을 반환
    

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data
    # 중복 username 확인
        username = data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError({"username": "A user with that username already exists."})

        # 중복 nickname 확인 (필요 시)
        nickname = data.get("nickname")
        if User.objects.filter(nickname=nickname).exists():
            raise ValidationError({"nickname": "A user with that nickname already exists."})
        # email
        email = data.get("email")
        # phone number
        phone_number = data.get('phone_number')
        user_email(user, email)
        user_username(user, username)
        if nickname:
            user_field(user, "nickname", nickname)
        if phone_number:
            user_field(user, 'phone_number', phone_number)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user