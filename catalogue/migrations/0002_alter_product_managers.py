# Generated by Django 3.2 on 2024-06-19 06:07

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
