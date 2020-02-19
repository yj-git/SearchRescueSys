from datetime import datetime

from rest_framework.decorators import APIView, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User


class CaseBaseView(APIView):
    def get_user(self, request):
        if hasattr(request, 'user'):
            user = getattr(request, 'user')
        return user
