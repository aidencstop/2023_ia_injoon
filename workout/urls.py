from django.urls import path
from .views import *

urlpatterns = [
    path('manage_workout/<str:member_id>/', manage_workout, name='manage_workout'),
]
