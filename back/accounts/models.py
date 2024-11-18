from django.db import models
from django.conf import settings

# User 모델: 사용자의 기본 정보를 저장하는 모델입니다.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)  # 사용자 이름
    email = models.EmailField(max_length=254, unique=True)  # 이메일 주소
    password = models.CharField(max_length=128)  # 비밀번호
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # 프로필 이미지
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