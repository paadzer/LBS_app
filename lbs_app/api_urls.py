from rest_framework import routers
from .views import BusinessViewSet, BusinessCategoryViewSet, ServiceAreaViewSet

router = routers.DefaultRouter()
router.register(r"businesses", BusinessViewSet, basename="business")
router.register(r"categories", BusinessCategoryViewSet, basename="category")
router.register(r"service-areas", ServiceAreaViewSet, basename="service-area")

urlpatterns = router.urls