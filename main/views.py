from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
import jwt
import random
import string
from django.conf import settings
from rest_framework.decorators import api_view
# Create your views here.

class CreateUserView(generics.CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = RegistrationSerializer


class LogoutView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message":"Successfully Logged OUT!"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ReferanceView(APIView):
    def post(self,request):
        request_data = JSONParser().parse(request)
        serializer = ReferenceSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        queryset = Reference.objects.all()
        serializer = ReferenceSerializer(queryset, many=True)
        return Response(serializer.data)
class DbInformationView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, client_id):
        try:
            queryset = DbInformation.objects.filter(client_id=client_id)
            serializer = DbInformationSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def post(self,request,client_id):
        request_data=JSONParser().parse(request)
        try:
            db_info={
                "client_id":client_id,
                "referance_id":request_data["referance_id"]
            }
            db_info_serializer=DbInformationSerializer(data=db_info)
            if db_info_serializer.is_valid():
                db_info_serializer.save()
                return Response(db_info_serializer.data,status=status.HTTP_201_CREATED)
            return Response(db_info_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print(e)
            return Response({"msg":str(e)},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,client_id):
        #delete entire table
        try:
            DbInformation.objects.filter(client_id=client_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class GetClientIdView(APIView):
    def get(self,request,token_id):
        try:
            token = ClientIdMapping.objects.get(token_id=token_id)
            return Response(ClientIdSerializer(token).data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def post(self,request,token_id):
        request_data=JSONParser().parse(request)
        try:
            token={
                'token_id':token_id,
                'client_id':request_data['client_id'],
            }
            token_serializer=ClientIdSerializer(data=token)
            if token_serializer.is_valid():
                token_serializer.save()
                return Response(token_serializer.data,status=status.HTTP_201_CREATED)
            return Response(token_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GenerateEthanTokenView(APIView):
    def get(self, request):
        #generate random token of size 64
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))
        # print(token)
        return Response({"data":token})

class DecodeEthanToken(APIView):
    def post(self, request):
        request_data=JSONParser().parse(request)
        try:
            token=request_data['token']
            client_mapping_data=ClientIdMapping.objects.get(ethan_token=token)
            client_id=client_mapping_data.client_id
            access=DbInformation.objects.filter(client_id=client_id)
            access_data=DbInformationSerializer(access,many=True)
            db_details=[]
            for access_data1 in access_data.data:
                referance_id=access_data1['referance_id']
                referance_data=Reference.objects.get(referance_id=referance_id)
                referance_data_serializer=ReferenceSerializer(referance_data)
                # print(referance_data_serializer.data)
                db_details.append(referance_data_serializer.data)
            return Response({"data":db_details},status=status.HTTP_200_OK)
        except Exception as e:
            # print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GetClientIdByEthanToken(APIView):
    def post(self,request):
        try:
            # request_data=JSONParser().parse(request)
            token=request.data['token']
            client_mapping_data=ClientIdMapping.objects.get(ethan_token=token)
            client_id=client_mapping_data.client_id
            return Response({"data":client_id},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"err":str(e)},status=status.HTTP_400_BAD_REQUEST)

class DecodeJwtView(APIView):
    def get(self,request):
        try:
            client_mapping_data=ClientIdMapping.objects.all()
            client_mapping_serializer=ClientIdMappingSerializer(client_mapping_data,many=True)
            return Response(client_mapping_serializer.data)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        request_data=JSONParser().parse(request)
        try:
            token=request_data['token']
            print(token)
            decoded_token=jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
            print(decoded_token)
            client_id=decoded_token['user_id']

            access=DbInformation.objects.filter(client_id=client_id)
            print(access)
            access_data=DbInformationSerializer(access,many=True)
            print(access_data)
            # print(access_data.data)
            db_details=[]
            for access_data1 in access_data.data:
                referance_id=access_data1['referance_id']
                referance_data=Reference.objects.get(referance_id=referance_id)
                referance_data_serializer=ReferenceSerializer(referance_data)
                # print(referance_data_serializer.data)
                db_details.append(referance_data_serializer.data)
                #connect to postgresql
            token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))
            # print(token)
            client_mapping_data={
                'client_id':client_id,
                'ethan_token':token
            }
            response={
                "token":token
            }
            client_mapping_serializer=ClientIdMappingSerializer(data=client_mapping_data)
            if client_mapping_serializer.is_valid():
                client_mapping_serializer.save()
                return JsonResponse(response,status=status.HTTP_201_CREATED)
            else:
                return Response(client_mapping_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print(e)
            return Response({"msg":"Invalid Token"},status=status.HTTP_400_BAD_REQUEST)
class UserDetailView(APIView):
    def post(self, request):
        if request.method =="POST":
            token = request.data['access_token']
            token_decoded = jwt.decode(token, key=settings.SECRET_KEY, algorithms=['HS256'])
            if token_decoded:
                alluser = list(NewUser.objects.values_list("username", 'phone_number', 'email', 'code'))
                username = str(NewUser.objects.get(id = token_decoded["user_id"]))
                myuser = {
                    "username":"",
                    "phone_number":"",
                    "email":"",
                    "code":""
                }
                for user in alluser:
                    if username == user[0]:
                        myuser["username"] = user[0]
                        myuser["phone_number"] = user[1]
                        myuser["email"] = user[2]
                        myuser["code"] = user[3]
                return Response(myuser)
            else:
                return Response({"message":"This token has either expired or invalid"})

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = NewUser.objects.all()
    permission_classes = []
class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = NewUser.objects.all()
    permission_classes = []
@api_view(['GET'])
def foo(request):
    return Response({"message":"Working"})

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
# class ClientIDView(APIView):


class ReferanceDetailView(APIView):
    def get(self, request):
        referance_id = request.query_params['reference_id']
        referance = Reference.objects.filter(referance_id = referance_id)
        print(referance)
        serializer = ReferenceSerializer(referance, many=True)
        print(serializer)
        response = serializer.data
        return JsonResponse({"response":response},status=status.HTTP_200_OK)

class TableauConnectView(APIView):
    def get(self, request):
        token = request.query_params['token']
        client_mapping_data=ClientIdMapping.objects.get(ethan_token=token)
        client_id=client_mapping_data.client_id
        tableaus = TableauConnection.objects.filter(client_id = client_id)
        serializer = TableauConnectionSerializer(tableaus, many =True)
        response = serializer.data
        return JsonResponse({"response":response},status=status.HTTP_200_OK)
    def post(self, request):
        token=request.data['token']
        tableau_id = request.data['tableau_id']
        client_mapping_data=ClientIdMapping.objects.get(ethan_token=token)
        client_id=client_mapping_data.client_id
        tableauConnect = TableauConnection(client_id = client_id, tableau_id = tableau_id)
        serializer=TableauConnectionSerializer(data= tableauConnect.__dict__)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"client_id": client_id, "tableau_id": tableau_id},status=status.HTTP_200_OK)

class TableauView(APIView):
    def get(self, request):
        tableau_id = request.query_params['tableau_id']
        tableaus = Tableau.objects.filter(id = tableau_id)
        serializer = TableauSerializer(tableaus, many =True)
        response = serializer.data
        return JsonResponse({"response":response},status=status.HTTP_200_OK)
    def post(self, request):
        sitename=request.data['sitename']
        password = request.data['password']
        user_id = request.data['user_id']
        tableau = Tableau(sitename = sitename, password = password, user_id = user_id)
        serializer=TableauSerializer(data= tableau.__dict__)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message":"tableau successfully created"},status=status.HTTP_200_OK)
