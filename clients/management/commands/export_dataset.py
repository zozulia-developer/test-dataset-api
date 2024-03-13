import csv
from datetime import date, datetime

from django.core.management.base import BaseCommand

from clients.models import Client


class Command(BaseCommand):
    help = 'Export data to CSV according to the specified filters'

    def add_arguments(self, parser):
        parser.add_argument('--category', help='Category filter')
        parser.add_argument('--gender', help='Gender filter')
        parser.add_argument('--min_age', type=int, help='Minimum age filter')
        parser.add_argument('--max_age', type=int, help='Maximum age filter')

    def handle(self, *args, **options):
        filters = {}
        if options['category']:
            filters['category'] = options['category']
        if options['gender']:
            filters['gender'] = options['gender']
        if options['min_age']:
            filters['birth_date__year__gte'] = date.today().year - options['min_age']
        if options['max_age']:
            filters['birth_date__year__lte'] = date.today().year - options['max_age'] - 1

        queryset = Client.objects.filter(**filters)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        with open(f'exported_data_{timestamp}.csv', 'w', newline='') as csvfile:
            fieldnames = ['category', 'firstname', 'lastname', 'email', 'gender', 'birth_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for client in queryset:
                writer.writerow({
                    'category': client.category,
                    'firstname': client.first_name,
                    'lastname': client.last_name,
                    'email': client.email,
                    'gender': client.gender,
                    'birth_date': client.birth_date,
                })
        self.stdout.write(self.style.SUCCESS('Data exported successfully'))
