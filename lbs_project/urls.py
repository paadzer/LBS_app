from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("lbs_app.api_urls")),
    path("", include("lbs_app.urls")),
]