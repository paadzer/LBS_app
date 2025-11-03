# Import REST Framework router for automatic URL generation
from rest_framework import routers
from .views import BusinessViewSet, BusinessCategoryViewSet, ServiceAreaViewSet

# Create a default router that automatically generates REST API URLs
router = routers.DefaultRouter()

# Register ViewSets with the router
# This automatically creates routes like /api/businesses/, /api/businesses/{id}/, etc.
router.register(r"businesses", BusinessViewSet, basename="business")
router.register(r"categories", BusinessCategoryViewSet, basename="category")
router.register(r"service-areas", ServiceAreaViewSet, basename="service-area")

# Export the router's URLs
urlpatterns = router.urls