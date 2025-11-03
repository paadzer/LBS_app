from django.contrib.gis.geos import Point, Polygon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lbs_app.models import Business, BusinessCategory, ServiceArea


class BusinessAPITests(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.category = BusinessCategory.objects.create(name="Restaurant", slug="restaurant")
        self.service_area = ServiceArea.objects.create(
            name="City Centre",
            boundary=Polygon((
                (-6.30, 53.34),
                (-6.20, 53.34),
                (-6.20, 53.37),
                (-6.30, 53.37),
                (-6.30, 53.34),
            ))
        )
        self.business = Business.objects.create(
            name="Test Bistro",
            category=self.category,
            service_area=self.service_area,
            description="Modern Irish cuisine",
            location=Point(-6.26, 53.35)
        )

    def test_list_businesses(self):
        """Test listing all businesses"""
        response = self.client.get(reverse("business-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_business_detail(self):
        """Test retrieving a single business"""
        response = self.client.get(reverse("business-detail", args=[self.business.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Bistro")

    def test_nearby_search(self):
        """Test spatial query for nearby businesses"""
        response = self.client.get(reverse("business-nearby"), {
            "lat": 53.35,
            "lon": -6.26,
            "radius": 1500
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_nearest_search(self):
        """Test spatial query for nearest businesses"""
        response = self.client.get(reverse("business-nearest"), {
            "lat": 53.35,
            "lon": -6.26,
            "limit": 3
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)