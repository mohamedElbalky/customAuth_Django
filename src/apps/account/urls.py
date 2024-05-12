from django.urls import path

from . import views




app_name = 'account'



urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify/<str:token>/', views.verify_email_view, name='verify_token'),
    
    path('login/', views.login_view, name='login'),
    
    path('user/', views.user_list_view, name='user_list'),
    path('user/me/', views.user_detail_view, name='user_detail'),
    path('user/me/edit/', views.edit_user_info, name='user_info_edit'),
    path('user/me/edit/avatar', views.change_avatar_view, name='user_avatar_edit'),
    
]
