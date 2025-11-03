from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Business, BusinessCategory, ServiceArea


class GeoJSONField(serializers.Field):
    """Custom field to serialize GeoDjango geometry to GeoJSON"""
    def to_representation(self, value):
        if value:
            return {
                'type': value.geom_type,
                'coordinates': value.coords
            }
        return None


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = ["id", "name", "slug", "description"]


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ["id", "name", "boundary", "created_at"]


class BusinessSerializer(serializers.ModelSerializer):
    category = BusinessCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BusinessCategory.objects.all(), 
        source="category", 
        write_only=True
    )
    service_area = ServiceAreaSerializer(read_only=True)
    service_area_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceArea.objects.all(), 
        source="service_area", 
        write_only=True, 
        allow_null=True
    )
    location = GeoJSONField()

    class Meta:
        model = Business
        fields = [
            "id",
            "name",
            "description",
            "phone",
            "email",
            "website",
            "location",
            "category",
            "category_id",
            "service_area",
            "service_area_id",
            "created_at",
            "updated_at",
        ]