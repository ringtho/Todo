from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Task

# Create your models here.
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']
        extra_kwargs = {
            "password":{"write_only":True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class LogoutSerializer(ModelSerializer):
    refresh = serializers.CharField()

    class Meta:
        model = User
        fields = ['refresh']

    default_error_message = {
        'bad_token':('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken().blacklist()
        except TokenError:
            self.fail('bad_token')
            

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title','description','complete']