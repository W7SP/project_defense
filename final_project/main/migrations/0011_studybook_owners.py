# Generated by Django 4.0.3 on 2022-03-26 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_account_balance'),
        ('main', '0010_equipment_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='studybook',
            name='owners',
            field=models.ManyToManyField(to='accounts.profile'),
        ),
    ]
