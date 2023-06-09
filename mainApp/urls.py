from django.urls import path
from . import views
from .views import activate

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio-list/', views.portfolios_list, name='portfolio-list'),
    path('favorite/', views.favorite, name='favorite'),
    path('like/', views.like, name='like'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),

    path('chat/<str:username>', views.chat, name='chat'),
    path('chat/', views.chat_template, name='chat_template'),
    path('send/', views.send, name='send'),
    path('getMessages/<str:username>/', views.get_messages, name='get-messages'),

    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('watch-portfolio/<str:username>/', views.watch_portfolio, name='watch-portfolio'),
    path('edit-portfolio/', views.edit_portfolio, name='edit-portfolio'),

    path('about/', views.about, name='about')
]
