# Import REST Framework serializers for API data conversion
from rest_framework import serializers
# Import Point geometry type for validation
from django.contrib.gis.geos import Point
# Import our models
from .models import Business, BusinessCategory, ServiceArea


class GeoJSONField(serializers.Field):
    """
    Custom field to serialize GeoDjango geometry to GeoJSON format
    
    By default, PostGIS returns WKT (Well-Known Text) format like "SRID=4326;POINT(-6.26 53.34)".
    This custom field converts it to standard GeoJSON format that JavaScript map libraries expect:
    {"type": "Point", "coordinates": [-6.26, 53.34]}
    """
    def to_representation(self, value):
        # If we have a geometry value, convert it to GeoJSON format
        if value:
            return {
                'type': value.geom_type,      # e.g., "Point", "Polygon"
                'coordinates': value.coords   # e.g., [-6.26, 53.34] for a Point
            }
        # Return None if there's no geometry
        return None


class BusinessCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for BusinessCategory model
    
    Converts business category objects to/from JSON for API responses.
    """
    class Meta:
        # Specify which model this serializer works with
        model = BusinessCategory
        # Specify which fields to include in the JSON output
        fields = ["id", "name", "slug", "description"]


class ServiceAreaSerializer(serializers.ModelSerializer):
    """
    Serializer for ServiceArea model
    
    Converts service area objects (with polygons) to/from JSON for API responses.
    """
    class Meta:
        # Specify which model this serializer works with
        model = ServiceArea
        # Specify which fields to include in the JSON output
        fields = ["id", "name", "boundary", "created_at"]


class BusinessSerializer(serializers.ModelSerializer):
    """
    Serializer for Business model with nested relationships
    
    Handles complex business objects including nested category and service area data.
    """
    # Nested serializer: when reading (GET), show full category details
    category = BusinessCategorySerializer(read_only=True)
    # Write-only field: when creating/updating (POST/PUT), accept category ID
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BusinessCategory.objects.all(),  # Valid categories user can choose from
        source="category",                         # Map this field to the category property
        write_only=True                           # Only used for writing, not reading
    )
    # Nested serializer: when reading (GET), show full service area details
    service_area = ServiceAreaSerializer(read_only=True)
    # Write-only field: when creating/updating (POST/PUT), accept service area ID
    service_area_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceArea.objects.all(),      # Valid service areas user can choose from
        source="service_area",                    # Map this field to the service_area property
        write_only=True,                          # Only used for writing, not reading
        allow_null=True                          # Service area is optional
    )
    # Use our custom GeoJSON field to convert locations properly
    location = GeoJSONField()

    class Meta:
        # Specify which model this serializer works with
        model = Business
        # Specify all fields to include in the JSON output
        fields = [
            "id",
            "name",
            "description",
            "phone",
            "email",
            "website",
            "location",          # GeoJSON formatted location
            "category",          # Full category details (read-only)
            "category_id",       # Category ID for updates (write-only)
            "service_area",      # Full service area details (read-only)
            "service_area_id",   # Service area ID for updates (write-only)
            "created_at",
            "updated_at",
        ]