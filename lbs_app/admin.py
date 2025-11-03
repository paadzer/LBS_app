from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Business, BusinessCategory, ServiceArea


@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(ServiceArea)
class ServiceAreaAdmin(OSMGeoAdmin):
    """ServiceArea admin with OpenStreetMap integration"""
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Business)
class BusinessAdmin(OSMGeoAdmin):
    """Business admin with map-based geometry editing"""
    list_display = ("name", "category", "service_area", "created_at")
    list_filter = ("category", "service_area")
    search_fields = ("name", "description", "category__name")
    default_lon = -6.2603
    default_lat = 53.3498
    default_zoom = 12