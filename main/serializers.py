from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        # data.update({'email': self.user.email})
        # data.update({'username': self.user.username})
        # data.update({'phoneNumber': self.user.phone_number})
        # data.update({'code': self.user.code})
        # and everything else you want to send in the response
        return data

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NewUser
#         fields = ("username", 'phone_number', 'email', 'code')


class ClientIdMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientIdMapping
        fields = ("client_id", 'ethan_token')
class ClientIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientIdMapping
        fields = ("client_id", 'ethan_token')

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ("referance_id","ref_type", 'field1', 'field2', 'field3', 'field4', 'field5')
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):

        user = NewUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            code=validated_data['code'],
        )
        return user
    def post(self, request):
        if request.METHOD == "POST":
            print(request)
    class Meta:
        model = NewUser
        fields = ("id", "username", "password", 'phone_number', 'email', 'code')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ("__all__")

class DbInformationSerializer(serializers.ModelSerializer):
    # referance_id = ReferenceSerializer()
    class Meta:
        model = DbInformation
        fields = ("client_id", 'referance_id')

class TableauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tableau
        fields = ("__all__")

class TableauConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableauConnection
        fields = ("__all__")