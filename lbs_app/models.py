from django.contrib.gis.db import models
from django.utils import timezone


class BusinessCategory(models.Model):
    """Business categories for classification"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    """Service area polygons for spatial containment queries"""
    name = models.CharField(max_length=150, unique=True)
    boundary = models.PolygonField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Business(models.Model):
    """Business locations as spatial points"""
    category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE, related_name="businesses")
    service_area = models.ForeignKey(
        ServiceArea, 
        on_delete=models.SET_NULL, 
        related_name="businesses", 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    location = models.PointField(srid=4326)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["service_area"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name