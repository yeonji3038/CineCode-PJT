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
