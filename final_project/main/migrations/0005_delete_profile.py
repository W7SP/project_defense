# Generated by Django 4.0.3 on 2022-03-22 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_equipment_remove_profile_user_delete_trainer_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
