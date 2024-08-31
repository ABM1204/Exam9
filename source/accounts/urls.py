from django.urls import path
from .views import RegistrationView, UserLoginView, UserLogoutView, UserProfileView, UserFavoritesView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('favorites/', UserFavoritesView.as_view(), name='user_favorites'),
]
