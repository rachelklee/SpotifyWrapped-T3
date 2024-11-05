from django.urls import path
from .views import main, login_user, logout_user, delete_user, display_user
from . import views

app_name = 'api'

urlpatterns = [
    path('home', main),
    path('', main),
    path('register/', views.register_user, name='register_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.display_user, name='display_user'),
    path('delete_wraps/', views.delete_wraps, name='delete_wraps'),
]
