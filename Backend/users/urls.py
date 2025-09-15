from django.urls import path
from .views import User_APIView

urlpatterns = [
    path('', User_APIView.as_view())
]