from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ProfileListCreateAPIView, ProfileRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('register/', ProfileListCreateAPIView.as_view(), name='profile-list-create'),
    path('profiles/<str:user_id>/', ProfileRetrieveUpdateDestroyAPIView.as_view(), name='profile-retrieve-update-destroy'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

