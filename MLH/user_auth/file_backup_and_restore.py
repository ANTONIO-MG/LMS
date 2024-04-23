import json
from django.core.serializers.json import DjangoJSONEncoder
from models import *

def backup_data(models):
    backup_data = {}
    for model in models:
        model_name = model.__name__
        queryset = model.objects.all()
        serialized_data = json.dumps(
            list(queryset.values()), cls=DjangoJSONEncoder)
        backup_data[model_name] = serialized_data

    with open('backup.json', 'w') as backup_file:
        json.dump(backup_data, backup_file)


def restore_data(models):
    with open('backup.json', 'r') as backup_file:
        backup_data = json.load(backup_file)

    for model in models:
        model_name = model.__name__
        serialized_data = backup_data.get(model_name, '[]')
        objects_data = json.loads(serialized_data)

        for obj_data in objects_data:
            model.objects.create(**obj_data)


# Usage example:
models_to_backup = [Person, Classroom, Notification,
                    Message, TODO, Subject, Post, TaskCompletion]

# Backup data

# Restore data
def  backup():
    print("Starting to backup all data to databases based on file backup")
    backup_data(models_to_backup)
    print("backup completed")


# Drop the existing data in the models (use with caution)
# def  drop_data(models):
#     print("dropping all tables on database")
#     for model in models_to_backup:
#         model.objects.all().delete()
#         print("All tables dropped")

# # Restore data
# def  restore():
#     print("Starting to restore all data to databases based on file backup")
#     restore_data(models_to_backup)
#     print("Restore completed")

backup()