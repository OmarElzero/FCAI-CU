from django.core.management.base import BaseCommand
from reservations.models import Location

class Command(BaseCommand):
    help = 'Create sample locations for reservations'
    
    def handle(self, *args, **options):
        locations = [
            {
                'name': 'Main Auditorium',
                'description': 'Large auditorium with 500 seats',
                'capacity': 500,
                'facilities': 'Projector, Sound system, Stage, Microphones',
                'available_for_carnival': True,
                'available_for_creativa': True,
            },
            {
                'name': 'Conference Room A',
                'description': 'Modern conference room for meetings',
                'capacity': 50,
                'facilities': 'Smart TV, Whiteboard, Air conditioning',
                'available_for_carnival': False,
                'available_for_creativa': True,
            },
            {
                'name': 'Lab 1',
                'description': 'Computer lab with 30 computers',
                'capacity': 30,
                'facilities': '30 Computers, Projector, Air conditioning',
                'available_for_carnival': True,
                'available_for_creativa': True,
            },
            {
                'name': 'Sports Hall',
                'description': 'Large sports hall for physical activities',
                'capacity': 200,
                'facilities': 'Sound system, Sports equipment storage',
                'available_for_carnival': True,
                'available_for_creativa': False,
            },
            {
                'name': 'Library Study Room',
                'description': 'Quiet study room for small groups',
                'capacity': 20,
                'facilities': 'Tables, Chairs, Whiteboard, Quiet environment',
                'available_for_carnival': False,
                'available_for_creativa': True,
            },
        ]
        
        for location_data in locations:
            location, created = Location.objects.get_or_create(
                name=location_data['name'],
                defaults=location_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created location: {location.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Location already exists: {location.name}')
                )