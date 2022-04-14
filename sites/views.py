from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def get_queryset(self):
        """
        IT Admin should get access to all sites
        Manager should get access to managed sites
        Cleaner should get access to sites where they work.
        """
        current_user = self.request.user
        group = current_user.groups.values_list('name', flat=True).first()
        if group == 'IT Admin':
            return Site.objects.all()
        if group == 'Managers':
            return Site.objects.filter(manager=current_user)
        return Site.objects.filter(job_sites__cleaner=current_user)


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        current_user = self.request.user
        group = current_user.groups.values_list('name', flat=True).first()
        if group == 'Cleaners':
            return Job.objects.filter(cleaner=current_user)
        return Job.objects.all()


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        current_user = self.request.user
        group = current_user.groups.values_list('name', flat=True).first()
        if group == 'Cleaners':
            return Schedule.objects.filter(cleaner=current_user)
        return Schedule.objects.all()


class ProductOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
