from multiprocessing import context
import requests
from rest_framework.request import Request
from rest_framework.response import Response
from django.http.request import HttpRequest
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth.models import Group
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer, GroupSerializer
import os
from rest_framework import filters

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

IP_token = 'https://worklink.herokuapp.com/o/token/'


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retriving all the employee details or a specific employee
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'groups__name']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def getuser(self, request: HttpRequest):
        current_user = self.request.user
        user_model = Employee.objects.filter(email=current_user)
        serializer_context = {
            'request': request
        }
        serializer = EmployeeSerializer(
            user_model, many=True, context=serializer_context)
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View for retriving all the groups details or a specific group/
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


"""
token view
CODE FROM CLOUD COMPUTING MODULE
description slightly modifies to say email rather than username.
"""


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with email and password. Input should be in the format:
    {"username": "email", "password": "1234abcd"}
    '''
    r = requests.post(
        IP_token,
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())
