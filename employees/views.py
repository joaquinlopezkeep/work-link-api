import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import Group
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer, GroupSerializer
from decouple import config


CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')

IP_token = 'http://127.0.0.1:8000/o/token/'


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retriving all the employee details or a specific employee
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This method is overridden to enable Managers and IT admin to see all user but
        Cleaners can only see their profile.
        """
        current_user = self.request.user
        group = current_user.groups.values_list('name', flat=True).first()
        if(group == 'IT Admin' or group == 'Managers'):
            return Employee.objects.all()
        return Employee.objects.filter(email=current_user)


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
