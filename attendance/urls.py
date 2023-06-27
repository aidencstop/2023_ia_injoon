from django.urls import path
from .views import *

urlpatterns = [
    path('manage_attendance/<str:member_id>/', manage_attendance, name='manage_attendance'),
]
