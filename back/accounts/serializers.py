from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.core.validators import RegexValidator


class UserSerializer(RegisterSerializer):
    phoneNumberRegex = RegexValidator(
        regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
        message="휴대폰 번호는 다음과 같은 형식을 따라야 합니다: 010-1234-5678"
    )
    phone_number = serializers.CharField(
        validators=[phoneNumberRegex],
        required=True,
        help_text="휴대폰 번호는 다음과 같은 형식을 따라야 합니다: 010-1234-5678"
    )

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.validated_data.get('phone_number')
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'profile_image')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
            'profile_image': {'required': False}
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)


# 기존 UserUpdateSerializer는 그대로 두고 아래 클래스를 추가합니다class UserProfileSerializer(serializers.ModelSerializer):
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'profile_image')
        read_only_fields = ('username',)