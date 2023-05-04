from django.urls import path
from . import views
from .views import activate, reset_password

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('recovery/', views.recoveryPage, name='recovery'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', reset_password, name='reset_password'),
    path('chat/<str:pk>', views.chat, name='chat')
]
