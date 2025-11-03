# Import URL routing functions
from django.urls import path
from .views import IndexView

# Namespace for this app's URLs
app_name = "lbs_app"

# URL patterns for the main application (non-API routes)
urlpatterns = [
    # Homepage route - maps root URL to IndexView
    path("", IndexView.as_view(), name="home"),
]