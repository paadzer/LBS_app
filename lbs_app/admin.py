# Import Django admin and GeoDjango's OpenStreetMap admin
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
# Import our models
from .models import Business, BusinessCategory, ServiceArea


@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for BusinessCategory model
    
    Simple admin interface for managing business categories with search functionality.
    """
    # Fields to display in the list view
    list_display = ("name", "slug")
    # Fields that can be searched in the admin interface
    search_fields = ("name", "slug")


@admin.register(ServiceArea)
class ServiceAreaAdmin(OSMGeoAdmin):
    """
    Admin configuration for ServiceArea model with map integration
    
    Uses OSMGeoAdmin to provide an OpenStreetMap interface for drawing and editing polygons.
    """
    # Fields to display in the list view
    list_display = ("name", "created_at")
    # Fields that can be searched in the admin interface
    search_fields = ("name",)


@admin.register(Business)
class BusinessAdmin(OSMGeoAdmin):
    """
    Admin configuration for Business model with map-based location editing
    
    Uses OSMGeoAdmin to provide an OpenStreetMap interface for setting business locations.
    """
    # Fields to display in the list view
    list_display = ("name", "category", "service_area", "created_at")
    # Add filters on the right sidebar for these fields
    list_filter = ("category", "service_area")
    # Fields that can be searched in the admin interface
    search_fields = ("name", "description", "category__name")
    # Default map view centered on Dublin, Ireland
    default_lon = -6.2603
    default_lat = 53.3498
    default_zoom = 12