from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model


def create_no_class(sender, **kwargs):
    from .models import Classroom
    Classroom.objects.get_or_create(name='NO CLASS', defaults={'description': 'Default class for new users'})

def create_admin_user(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='Admin1234',
            first_name='Admin',
            last_name='Account',
            is_staff=True,
            is_superuser=True
        )

class UsersAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users_auth'

    def ready(self):
        import users_auth.signals
        post_migrate.connect(create_no_class, sender=self)
        post_migrate.connect(create_admin_user, sender=self)




        