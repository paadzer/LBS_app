# Import random number generator
import random
# Import Point geometry for creating spatial locations
from django.contrib.gis.geos import Point
# Import base command class for Django management commands
from django.core.management.base import BaseCommand
# Import our models
from lbs_app.models import Business, BusinessCategory, ServiceArea


class Command(BaseCommand):
    """
    Django management command to generate random businesses for testing
    
    This command creates sample business data across multiple cities and categories.
    Usage: python manage.py generate_businesses --count 100
    """
    help = 'Generate random businesses for testing'

    def add_arguments(self, parser):
        # Add --count argument to specify how many businesses to create
        parser.add_argument('--count', type=int, default=100, help='Number of businesses to generate')

    def handle(self, *args, **options):
        # Get the count from command line arguments
        count = options['count']
        
        # Get or create the three main business categories
        # These will be created if they don't exist, otherwise retrieved
        restaurant_category, _ = BusinessCategory.objects.get_or_create(
            slug='restaurant',
            defaults={'name': 'Restaurant', 'description': 'Dining establishments'}
        )
        retail_category, _ = BusinessCategory.objects.get_or_create(
            slug='retail',
            defaults={'name': 'Retail', 'description': 'Shops and stores'}
        )
        services_category, _ = BusinessCategory.objects.get_or_create(
            slug='services',
            defaults={'name': 'Services', 'description': 'Professional services'}
        )
        
        # List of all categories for random selection
        categories = [restaurant_category, retail_category, services_category]
        
        # Define locations around the world where businesses will be created
        locations = [
            # Ireland - All counties with 5 businesses each
            {"name": "Dublin Restaurants", "lat": 53.3498, "lon": -6.2603, "count": 5, "country": "Ireland"},
            {"name": "Dublin Retail", "lat": 53.3498, "lon": -6.2603, "count": 5, "country": "Ireland"},
            {"name": "Cork Restaurants", "lat": 51.8985, "lon": -8.4756, "count": 5, "country": "Ireland"},
            {"name": "Cork Retail", "lat": 51.8985, "lon": -8.4756, "count": 5, "country": "Ireland"},
            {"name": "Galway Restaurants", "lat": 53.2707, "lon": -9.0568, "count": 5, "country": "Ireland"},
            {"name": "Galway Services", "lat": 53.2707, "lon": -9.0568, "count": 5, "country": "Ireland"},
            {"name": "Limerick Restaurants", "lat": 52.6680, "lon": -8.6305, "count": 5, "country": "Ireland"},
            {"name": "Waterford Retail", "lat": 52.2593, "lon": -7.1119, "count": 5, "country": "Ireland"},
            {"name": "Kilkenny Services", "lat": 52.6541, "lon": -7.2552, "count": 5, "country": "Ireland"},
            {"name": "Wexford Restaurants", "lat": 52.3369, "lon": -6.4636, "count": 5, "country": "Ireland"},
            
            # Europe
            {"name": "London Business", "lat": 51.5074, "lon": -0.1278, "count": 3, "country": "UK"},
            {"name": "Paris Business", "lat": 48.8566, "lon": 2.3522, "count": 3, "country": "France"},
            {"name": "Berlin Business", "lat": 52.5200, "lon": 13.4050, "count": 3, "country": "Germany"},
            {"name": "Rome Business", "lat": 41.9028, "lon": 12.4964, "count": 3, "country": "Italy"},
            {"name": "Madrid Business", "lat": 40.4168, "lon": -3.7038, "count": 3, "country": "Spain"},
            {"name": "Amsterdam Business", "lat": 52.3676, "lon": 4.9041, "count": 3, "country": "Netherlands"},
            
            # Americas
            {"name": "New York Business", "lat": 40.7128, "lon": -74.0060, "count": 3, "country": "USA"},
            {"name": "Los Angeles Business", "lat": 34.0522, "lon": -118.2437, "count": 3, "country": "USA"},
            {"name": "San Francisco Business", "lat": 37.7749, "lon": -122.4194, "count": 3, "country": "USA"},
            {"name": "Toronto Business", "lat": 43.6532, "lon": -79.3832, "count": 3, "country": "Canada"},
            {"name": "Mexico City Business", "lat": 19.4326, "lon": -99.1332, "count": 3, "country": "Mexico"},
            
            # Asia-Pacific
            {"name": "Tokyo Business", "lat": 35.6762, "lon": 139.6503, "count": 3, "country": "Japan"},
            {"name": "Seoul Business", "lat": 37.5665, "lon": 126.9780, "count": 3, "country": "South Korea"},
            {"name": "Sydney Business", "lat": -33.8688, "lon": 151.2093, "count": 3, "country": "Australia"},
            {"name": "Melbourne Business", "lat": -37.8136, "lon": 144.9631, "count": 3, "country": "Australia"},
            {"name": "Singapore Business", "lat": 1.3521, "lon": 103.8198, "count": 3, "country": "Singapore"},
        ]
        
        # Dictionary of business name suffixes for each category
        business_names = {
            'restaurant': ['Cafe', 'Restaurant', 'Bistro', 'Pizzeria', 'Tavern', 'Pub', 'Bar', 'Diner', 'Eatery', 'Kitchen'],
            'retail': ['Store', 'Shop', 'Boutique', 'Market', 'Gallery', 'Emporium', 'Outlet', 'Mall', 'Bazaar', 'Mart'],
            'services': ['Tours', 'Guides', 'Services', 'Solutions', 'Consulting', 'Agency', 'Studio', 'Office', 'Center', 'Hub'],
        }
        
        # Keep track of how many businesses we've created
        created = 0
        
        # Loop through each location and create businesses
        for loc in locations:
            for i in range(loc['count']):
                # Randomly select a category
                category = random.choice(categories)
                # Get a random business name suffix for this category
                name_prefix = random.choice(business_names[category.slug])
                
                # Add random offset to spread businesses around (prevent all at exact same location)
                # 0.1 degrees ≈ 11km, so businesses are spread within ~11km of the center
                lat = loc['lat'] + random.uniform(-0.1, 0.1)
                lon = loc['lon'] + random.uniform(-0.1, 0.1)
                
                # Create the business with generated data
                business = Business.objects.create(
                    name=f"{loc['name'].split()[0]} {name_prefix} {i+1}",
                    description=f"A local business in {loc['name']}",
                    category=category,
                    location=Point(lon, lat),  # Create a Point geometry for the location
                    phone=f"+{random.randint(100000000, 999999999)}",
                    email=f"info@{loc['name'].lower().replace(' ', '')}.com",
                )
                created += 1
                
                # Stop if we've reached the requested count
                if created >= count:
                    break
            
            # Stop outer loop if we've reached the requested count
            if created >= count:
                break
        
        # Display success message with count of created businesses
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created} businesses'))