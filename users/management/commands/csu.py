from django.core.management import BaseCommand

from config.settings import TG_ID
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='nikkot198@gmail.com',
            first_name='Admin',
            last_name='Nikkot',
            is_staff=True,
            is_superuser=True,
            tg_id=TG_ID
        )

        user.set_password('123qwe')
        user.save()
