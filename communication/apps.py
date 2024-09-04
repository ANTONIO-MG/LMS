from django.apps import AppConfig

# The CommunicationConfig class is used to configure the 'communication' application.
# This class inherits from Django's AppConfig class, which provides the necessary
# configuration for the application.
class CommunicationConfig(AppConfig):
    # Specifies the default type of primary key to be used for models in this app.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name attribute specifies the full Python path to the application.
    name = 'communication'