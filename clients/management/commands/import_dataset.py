import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from clients.models import Client


class Command(BaseCommand):
    help = 'Populate the Client model with data from a .csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the .csv file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        clients_to_create = []

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = row['category']
                first_name = row['firstname']
                last_name = row['lastname']
                email = row['email']
                gender = row['gender']
                birth_date = datetime.strptime(row['birthDate'], '%Y-%m-%d').date()
                clients_to_create.append(
                    Client(
                        category=category,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        gender=gender,
                        birth_date=birth_date
                    )
                )

        existing_emails = set(Client.objects.values_list('email', flat=True))
        clients_to_save = [client for client in clients_to_create if client.email not in existing_emails]

        if clients_to_save:
            try:
                Client.objects.bulk_create(clients_to_save, batch_size=1000)
                self.stdout.write(self.style.SUCCESS('Successfully populated the Client model'))
            except IntegrityError as e:
                self.stdout.write(self.style.WARNING(f'Failed to create clients: {e}'))
        else:
            self.stdout.write(self.style.WARNING('No new clients to create.'))
