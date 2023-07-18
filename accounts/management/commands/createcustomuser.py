from getpass import getpass
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a custom user'

    def handle(self, *args, **options):
        username = input('Username: ')
        email = input('Email: ')
        name = input('Name: ')
        document = input('Document: ')
        
        while True:
            password1 = getpass('Password: ')
            password2 = getpass('Confirm Password: ')
            
            if password1 != password2:
                self.stdout.write(self.style.ERROR('Passwords do not match. Please try again.'))
            else:
                break

        try:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                name=name,
                document=document,
                password=password1,
            )

            self.stdout.write(self.style.SUCCESS(f'Custom user {username} created successfully.'))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(', '.join(e.messages)))
