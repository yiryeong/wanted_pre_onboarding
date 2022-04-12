from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password_check = serializers.CharField(
        style={'input_type': 'password', 'placeholder': '비민번호 확인'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password_check', 'email', 'is_staff']
        # 비밀번호는 보안상 암호화가 되었다 하더라도 클라이언트 측에 전달하지 못하게 하기 위해 write_only를 사용
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        account = User(
            email=validated_data['email'],
            username=validated_data['username'],
            is_staff=validated_data['is_staff'],
        )
        password = validated_data['password']
        password_check = validated_data['password_check']

        if password != password_check:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})

        account.set_password(password)
        account.save()

        return account

