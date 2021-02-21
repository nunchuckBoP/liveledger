# Generated by Django 3.1.4 on 2021-01-04 05:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='shared_with',
            field=models.ManyToManyField(null=True, related_name='shared_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
