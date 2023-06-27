from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('add_a_new_member/', add_a_new_member, name='add_a_new_member'),
    path('member_list/', member_list, name='member_list'),
    path('edit_member_info/<int:pk>/', edit_member_info, name='edit_member_info'),
    path('restore_members/', restore_members, name='restore_members'),
    path('admin_login/', admin_login, name='admin_login'),
    path('member_login/', member_login, name='member_login'),
    path('check_in_or_out/', check_in_or_out, name='check_in_or_out'),
    path('check_in/', check_in, name='check_in'),
    path('check_out/', check_out, name='check_out'),
]
