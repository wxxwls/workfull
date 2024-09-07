from rest_framework import serializers
from .models import *
from datetime import date
from django.contrib.auth import authenticate

from rest_framework import serializers
from .models import MyUser

class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)  # 일반 필드로 정의

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'birth_date', 'gender', 'phone_number']  # 모든 필드 포함
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        비밀번호와 비밀번호 확인 필드가 일치하는지 확인
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # password_confirm 필드는 실제 사용자 생성에 필요 없으므로 제거
        validated_data.pop('password_confirm')
        user = MyUser.objects.create_user(
            id=validated_data['id'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            birth_date=validated_data['birth_date'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number']
        )
        return user



class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(label="ID")
    password = serializers.CharField(write_only=True, label="비밀번호")
class LoginSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        id = data.get('id')
        password = data.get('password')

        if id and password:
            user = authenticate(id=id, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is deactivated.")
                return data
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'id' and 'password'.")
        
class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.ReadOnlyField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at', 'image', 'total_likes', 'liked_by_user']
        read_only_fields = ['created_at']

    def get_liked_by_user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user in obj.likes.all()
        return False 
    
class QnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = qna
        fields = ['id', 'title1', 'content1', 'title2', 'content2', 'title3', 'content3', 'title4', 'content4', 'title5', 'content5']