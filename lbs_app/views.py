from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.views.generic import TemplateView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Business, BusinessCategory, ServiceArea
from .serializers import (
    BusinessSerializer, 
    BusinessCategorySerializer, 
    ServiceAreaSerializer
)


class IndexView(TemplateView):
    """Main homepage view"""
    template_name = "lbs_app/index.html"


class BusinessViewSet(viewsets.ModelViewSet):
    """ViewSet for Business CRUD and spatial queries"""
    queryset = Business.objects.select_related("category", "service_area").all()
    serializer_class = BusinessSerializer
    filterset_fields = ["category__slug", "service_area__name"]
    search_fields = ["name", "description"]

    def _parse_point(self, request):
        """Parse latitude/longitude from query params"""
        try:
            lat = float(request.query_params.get("lat"))
            lon = float(request.query_params.get("lon"))
            return Point(lon, lat, srid=4326)
        except (TypeError, ValueError):
            return None

    @action(detail=False, methods=["get"])
    def nearby(self, request):
        """
        Spatial Query #1: Find businesses within a radius (proximity search)
        Usage: /api/businesses/nearby/?lat=53.3498&lon=-6.2603&radius=1000
        """
        point = self._parse_point(request)
        radius = request.query_params.get("radius", "1000")
        
        if not point:
            return Response(
                {"detail": "lat and lon query params are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            radius = float(radius)
        except ValueError:
            return Response(
                {"detail": "radius must be numeric."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(
            location__distance_lte=(point, radius)
        ).annotate(
            distance=Distance("location", point)
        ).order_by("distance")
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def nearest(self, request):
        """
        Spatial Query #2: Find nearest N businesses (nearest neighbor)
        Usage: /api/businesses/nearest/?lat=53.3498&lon=-6.2603&limit=5
        """
        point = self._parse_point(request)
        limit = request.query_params.get("limit", "5")
        
        if not point:
            return Response(
                {"detail": "lat and lon query params are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            limit = int(limit)
        except ValueError:
            return Response(
                {"detail": "limit must be an integer."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().annotate(
            distance=Distance("location", point)
        ).order_by("distance")[:limit]
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def within_area(self, request):
        """
        Spatial Query #3: Find businesses within a polygon (containment)
        Usage: /api/businesses/within-area/?name=City Centre
        """
        name = request.query_params.get("name")
        if not name:
            return Response(
                {"detail": "name query param is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            area = ServiceArea.objects.get(name__iexact=name)
        except ServiceArea.DoesNotExist:
            return Response(
                {"detail": "Service area not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        queryset = self.get_queryset().filter(location__within=area.boundary)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BusinessCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for BusinessCategory CRUD"""
    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategorySerializer
    http_method_names = ["get", "post", "patch", "delete"]


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """ViewSet for ServiceArea CRUD"""
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
    http_method_names = ["get", "post", "patch", "delete"]