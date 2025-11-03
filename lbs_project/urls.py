# Import Django's URL routing functions
from django.contrib import admin
from django.urls import path, include

# Define the URL patterns for the entire application
urlpatterns = [
    # Admin interface at /admin/
    path("admin/", admin.site.urls),
    # API endpoints at /api/ (delegated to lbs_app.api_urls)
    path("api/", include("lbs_app.api_urls")),
    # Root/homepage URL (delegated to lbs_app.urls)
    path("", include("lbs_app.urls")),
]