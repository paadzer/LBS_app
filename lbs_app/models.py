# Import GeoDjango models for spatial database support
from django.contrib.gis.db import models
from django.utils import timezone


class BusinessCategory(models.Model):
    """
    Business categories for classification
    
    This model stores different types of businesses (e.g., Restaurant, Retail, Services).
    Each business must belong to a category, which helps with filtering and organization.
    """
    # Category name (e.g., "Restaurant", "Retail")
    name = models.CharField(max_length=100, unique=True)
    # URL-friendly version of the name (e.g., "restaurant", "retail")
    slug = models.SlugField(max_length=120, unique=True)
    # Optional description of what this category includes
    description = models.TextField(blank=True)

    class Meta:
        # Order categories alphabetically by name
        ordering = ["name"]

    def __str__(self):
        # Display the category name in admin interface
        return self.name


class ServiceArea(models.Model):
    """
    Service area polygons for spatial containment queries
    
    This model stores geographical areas as polygons (e.g., city boundaries, districts).
    Used to find all businesses within a specific area (spatial query #3: containment).
    """
    # Name of the service area (e.g., "City Centre")
    name = models.CharField(max_length=150, unique=True)
    # Polygon geometry defining the area boundary (using WGS84 coordinate system)
    boundary = models.PolygonField(srid=4326)
    # Timestamp when the area was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order service areas alphabetically by name
        ordering = ["name"]

    def __str__(self):
        # Display the service area name in admin interface
        return self.name


class Business(models.Model):
    """
    Business locations as spatial points
    
    This is the main model that stores business information and their geographical locations.
    Each business has a point location (latitude/longitude) used for spatial queries.
    """
    # Link to the business category (restaurant, retail, etc.)
    # CASCADE means if category is deleted, all businesses in that category are also deleted
    category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE, related_name="businesses")
    # Link to service area (optional - not all businesses must be in a specific area)
    # SET_NULL means if service area is deleted, business remains but with no service area
    service_area = models.ForeignKey(
        ServiceArea, 
        on_delete=models.SET_NULL, 
        related_name="businesses", 
        null=True, 
        blank=True
    )
    # Business name
    name = models.CharField(max_length=200)
    # Business description
    description = models.TextField(blank=True)
    # Contact phone number
    phone = models.CharField(max_length=20, blank=True)
    # Contact email address
    email = models.EmailField(blank=True)
    # Business website URL
    website = models.URLField(blank=True)
    # Point geometry for the business location (latitude/longitude using WGS84)
    # This is the key spatial field that enables location-based searches
    location = models.PointField(srid=4326)
    # Timestamp when business record was created
    created_at = models.DateTimeField(default=timezone.now)
    # Timestamp when business record was last updated (auto-updated on save)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order businesses alphabetically by name
        ordering = ["name"]
        # Database indexes to speed up queries on common fields
        indexes = [
            models.Index(fields=["name"]),           # Speed up name searches
            models.Index(fields=["category"]),       # Speed up category filtering
            models.Index(fields=["service_area"]),   # Speed up service area filtering
            models.Index(fields=["-created_at"]),    # Speed up sorting by creation date (newest first)
        ]
        # Note: PostGIS automatically creates a GIST index on the location field for spatial queries

    def __str__(self):
        # Display the business name in admin interface
        return self.name