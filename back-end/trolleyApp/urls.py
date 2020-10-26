from django.urls import path
from . import views

urlpatterns = [
    path('register/user/', views.register_user, name='register_user'),
    path('login/', views.login, name='login_user'),
    path('trolly/info/', views.get_trolly_info, name="trolly info"),
    path('register/trolly/', views.register_trolly, name="register trolly"),
    path('trolly/occupy/', views.occupy_trolly, name='occupy a trolly'),
    path('trolly/availables/', views.get_available_trollies, name="get available trollies"),
    path('trolly/free/', views.free_trolly, name="free a trolly"),
    path('trolly/add/', views.register_trolly_by_code, name="register the node") 
]
