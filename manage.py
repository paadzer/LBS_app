#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This is the main entry point for Django management commands.
You can run commands like: python manage.py runserver, python manage.py migrate, etc.
"""
import os
import sys


def main():
    """
    Run administrative tasks.
    
    This function sets up Django and executes commands from the command line.
    """
    # Set which settings module Django should use
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lbs_project.settings")
    try:
        # Import Django's command execution function
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Display helpful error if Django isn't installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command that was requested from the command line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    # Run the main function when this script is executed directly
    main()