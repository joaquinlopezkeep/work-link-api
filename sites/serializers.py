from rest_framework import fields, serializers
from .models import *


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    manager = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Site
        fields = '__all__'


class JobSerializer(serializers.HyperlinkedModelSerializer):
    cleaner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Job
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    frequency = fields.MultipleChoiceField(choices=DAYS_IN_WEEK)

    class Meta:
        model = Schedule
        fields = '__all__'


class ProductOrderSerializer(serializers.ModelSerializer):
    site = SiteSerializer(many=False, read_only=True)
    category = fields.MultipleChoiceField(choices=PRODUCT_CATEGORY)

    class Meta:
        model = ProductOrder
        fields = '__all__'
