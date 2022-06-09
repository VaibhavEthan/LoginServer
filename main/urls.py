from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from .views import *
urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair' ),
    path('refresh/',  TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CreateUserView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/', UserDetailView.as_view(), name = 'user'),
    path('user/<int:pk>', UserView.as_view(), name = 'userid'),
    # path('client_id/', ClientIDView.as_view(), name = 'userid'),
    path("users/", UserListView.as_view(), name="alluser"),
    path('db_information/<str:client_id>', DbInformationView.as_view(), name = 'db_information'),
    path('get_client_id/<str:token_id>', GetClientIdView.as_view(), name = 'get_client_id'),
    path('generate_ethan_token/', GenerateEthanTokenView.as_view(), name = 'generate_ethan_token'),
    path('decode_jwt/', DecodeJwtView.as_view(), name = 'decode_jwt'),
    path('referance/', ReferanceView.as_view(), name = 'referance'),
    path('decode_ethan_token/',DecodeEthanToken.as_view(), name = 'decode_ethan_token'),
    path('get_client_id_by_ethan_token/', GetClientIdByEthanToken.as_view(), name = 'get_client_id_by_ethan_token'),
    path('reference/', ReferanceDetailView.as_view()),
    path('tableau/', TableauView.as_view()),
    path('tableau_data/', TableauConnectView.as_view()),
]
