# Generated by Django 3.1.4 on 2021-01-04 05:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20210104_0551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
