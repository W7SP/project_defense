# Generated by Django 4.0.3 on 2022-03-26 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_account_balance'),
        ('main', '0012_rename_owner_equipment_owners'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='owners',
        ),
        migrations.AddField(
            model_name='equipment',
            name='owners',
            field=models.ManyToManyField(to='accounts.profile'),
        ),
    ]