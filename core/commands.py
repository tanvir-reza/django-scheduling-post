from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a sample Django user for testing login (username/password)'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help='Username for sample')
        parser.add_argument('--email', default='postman@example.com', help='Email for sample')
        parser.add_argument('--password', default='123456', help='Password for sample')
        parser.add_argument('--voucher', default=None, help='Optional voucher code for profile')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created Django user "{username}"'))
        else:
            user.set_password(password)
            user.email = email
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Updated Django user "{username}"'))
        voucher = options.get('voucher')
        if voucher:
            # Update profile voucher if an app-specific Profile model exists.
            try:
                from app.models import Profile
                profile, _ = Profile.objects.get_or_create(user=user)
                profile.voucher_code = voucher
                profile.save()
                self.stdout.write(self.style.SUCCESS(f'Created/Updated profile voucher for {username}'))
            except (ImportError, AttributeError):
                pass
        self.stdout.write(self.style.WARNING(f'Username: {username}, Password: {password}'))
