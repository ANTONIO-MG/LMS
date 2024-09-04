from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model

# Function to create an admin user if it doesn't already exist
def create_admin_user(sender, **kwargs):
    User = get_user_model()  # Get the user model
    # Check if an admin user already exists
    if not User.objects.filter(username='admin').exists():
        # Create a new superuser with the specified credentials
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='Admin1234',
            first_name='Admin',
            last_name='Account',
            is_staff=True,
            is_superuser=True
        )

# Configuration class for the users_auth app
class UsersAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users_auth'

    # Method that runs when the app is ready
    def ready(self):
        import users_auth.signals  # Import signals module
        # Connect the create_admin_user function to the post_migrate signal
        post_migrate.connect(create_admin_user, sender=self)