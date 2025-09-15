from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework import status
from django.http import Http404
# Create your views here.


class User_APIView(APIView):

    def get(self, request, format=None, *args, **kargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)