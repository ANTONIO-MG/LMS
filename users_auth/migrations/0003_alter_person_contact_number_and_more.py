# Generated by Django 5.0.4 on 2024-05-13 12:25

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth', '0002_alter_person_bio_alter_person_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='contact_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='person',
            name='emergency_contact',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]