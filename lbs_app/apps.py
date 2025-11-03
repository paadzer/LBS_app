# Import Django's app configuration class
from django.apps import AppConfig


class LbsAppConfig(AppConfig):
    """
    Configuration for the LBS application
    
    This class configures application-level settings for the lbs_app.
    """
    # Use BigAutoField as the default primary key type
    default_auto_field = "django.db.models.BigAutoField"
    # Name of the application
    name = "lbs_app"