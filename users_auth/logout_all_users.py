from django.contrib.sessions.models import Session

# Delete all session objects from the database, effectively logging out all users
close = Session.objects.all().delete()

# The 'close' variable holds the result of the delete operation, which is a tuple
# containing the number of deleted objects and a dictionary with the count of each type of deleted object
close