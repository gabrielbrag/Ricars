from getpass import getpass
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a custom user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username of the user')
        parser.add_argument('--email', type=str, help='Email of the user')
        parser.add_argument('--name', type=str, help='Name of the user')
        parser.add_argument('--document', type=str, help='Document of the user')
        parser.add_argument('--password', type=str, help='Password for the user')

    def handle(self, *args, **options):
        username = options['username'] or input('Username: ')
        email = options['email'] or input('Email: ')
        name = options['name'] or input('Name: ')
        document = options['document'] or input('Document: ')
        
        password = options['password'] or getpass('Password: ')
        password2 = options['password'] or getpass('Confirm Password: ')
        
        while password != password2:
            self.stdout.write(self.style.ERROR('Passwords do not match. Please try again.'))
            password = getpass('Password: ')
            password2 = getpass('Confirm Password: ')

        try:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                name=name,
                document=document,
                password=password,
            )

            self.stdout.write(self.style.SUCCESS(f'Custom user {username} created successfully.'))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(', '.join(e.messages)))
