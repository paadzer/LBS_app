# Import PostGIS spatial functions for distance calculations
from django.contrib.gis.db.models.functions import Distance
# Import Point geometry type for creating location points
from django.contrib.gis.geos import Point
# Import Django's generic view for rendering templates
from django.views.generic import TemplateView
# Import REST Framework components for building APIs
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Import our models
from .models import Business, BusinessCategory, ServiceArea
# Import serializers to convert models to/from JSON
from .serializers import (
    BusinessSerializer, 
    BusinessCategorySerializer, 
    ServiceAreaSerializer
)


class IndexView(TemplateView):
    """
    Main homepage view that renders the application's index page
    
    This is a simple view that displays the main HTML page with the search form and map.
    """
    # Specify which HTML template to render
    template_name = "lbs_app/index.html"


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Business CRUD operations and spatial queries
    
    This class handles all API operations for businesses including:
    - Creating, reading, updating, deleting business records
    - Three spatial queries: proximity search, nearest neighbor, containment
    - Name-based searching and filtering
    """
    # Get all businesses and include related category/service_area data in one query (efficient)
    queryset = Business.objects.select_related("category", "service_area").all()
    # Use our custom serializer to convert businesses to/from JSON
    serializer_class = BusinessSerializer
    # Allow filtering businesses by category slug or service area name
    filterset_fields = ["category__slug", "service_area__name"]
    # Allow searching businesses by name or description
    search_fields = ["name", "description"]

    def _parse_point(self, request):
        """
        Helper method to parse latitude and longitude from request parameters
        
        Extracts lat/lon from URL query parameters and converts them to a PostGIS Point object.
        Returns None if the parameters are missing or invalid.
        """
        try:
            # Get latitude and longitude from the request
            lat = float(request.query_params.get("lat"))
            lon = float(request.query_params.get("lon"))
            # Create a Point object (lon comes first in PostGIS format)
            return Point(lon, lat, srid=4326)
        except (TypeError, ValueError):
            # Return None if parameters are missing or not valid numbers
            return None

    @action(detail=False, methods=["get"])
    def nearby(self, request):
        """
        Spatial Query #1: Find businesses within a radius (proximity search)
        
        This query finds all businesses within a specified distance from a given point.
        Example usage: /api/businesses/nearby/?lat=53.3498&lon=-6.2603&radius=1000
        """
        # Parse the search location from request parameters
        point = self._parse_point(request)
        # Get the search radius (default to 1000 meters if not provided)
        radius = request.query_params.get("radius", "1000")
        
        # Validate that we have a valid search location
        if not point:
            return Response(
                {"detail": "lat and lon query params are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate that radius is a valid number
        try:
            radius = float(radius)
        except ValueError:
            return Response(
                {"detail": "radius must be numeric."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find all businesses within the specified radius
        # location__distance_lte means "location distance less than or equal to"
        # annotate adds a distance field to each result showing exact distance in meters
        # order_by sorts results from closest to farthest
        queryset = self.get_queryset().filter(
            location__distance_lte=(point, radius)  # PostGIS spatial filter
        ).annotate(
            distance=Distance("location", point)     # Calculate exact distance
        ).order_by("distance")                       # Sort by distance
        
        # Convert results to JSON format
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def nearest(self, request):
        """
        Spatial Query #2: Find nearest N businesses (nearest neighbor)
        
        This query finds the N closest businesses to a given point, regardless of distance.
        Example usage: /api/businesses/nearest/?lat=53.3498&lon=-6.2603&limit=5
        """
        # Parse the search location from request parameters
        point = self._parse_point(request)
        # Get how many results to return (default to 5 if not provided)
        limit = request.query_params.get("limit", "5")
        
        # Validate that we have a valid search location
        if not point:
            return Response(
                {"detail": "lat and lon query params are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate that limit is a valid integer
        try:
            limit = int(limit)
        except ValueError:
            return Response(
                {"detail": "limit must be an integer."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find the N nearest businesses
        # annotate calculates the distance to each business
        # order_by sorts by distance (closest first)
        # [:limit] returns only the first N results
        queryset = self.get_queryset().annotate(
            distance=Distance("location", point)  # Calculate distance to each business
        ).order_by("distance")[:limit]           # Sort and limit results
        
        # Convert results to JSON format
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def within_area(self, request):
        """
        Spatial Query #3: Find businesses within a polygon (containment)
        
        This query finds all businesses that are located inside a specific service area polygon.
        Example usage: /api/businesses/within-area/?name=City Centre
        """
        # Get the service area name from request parameters
        name = request.query_params.get("name")
        
        # Validate that a name was provided
        if not name:
            return Response(
                {"detail": "name query param is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to find the service area by name (case-insensitive search)
        try:
            area = ServiceArea.objects.get(name__iexact=name)
        except ServiceArea.DoesNotExist:
            # Return error if the service area doesn't exist
            return Response(
                {"detail": "Service area not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Find all businesses whose location is within the service area's polygon boundary
        # location__within is a PostGIS spatial operator that checks if a point is inside a polygon
        queryset = self.get_queryset().filter(location__within=area.boundary)
        
        # Convert results to JSON format
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BusinessCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BusinessCategory CRUD operations
    
    Handles creating, reading, updating, and deleting business categories.
    """
    # Get all business categories
    queryset = BusinessCategory.objects.all()
    # Use the business category serializer
    serializer_class = BusinessCategorySerializer
    # Allow GET, POST, PATCH, DELETE methods (no PUT)
    http_method_names = ["get", "post", "patch", "delete"]


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ServiceArea CRUD operations
    
    Handles creating, reading, updating, and deleting service areas (geographical boundaries).
    """
    # Get all service areas
    queryset = ServiceArea.objects.all()
    # Use the service area serializer
    serializer_class = ServiceAreaSerializer
    # Allow GET, POST, PATCH, DELETE methods (no PUT)
    http_method_names = ["get", "post", "patch", "delete"]