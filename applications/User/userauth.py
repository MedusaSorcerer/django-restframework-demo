#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import uuid

from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class UserLoginAPIView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer


class UserLogoutAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user.user_secret = uuid.uuid4()
        user.save()
        return Response({'detail': 'login out.', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
