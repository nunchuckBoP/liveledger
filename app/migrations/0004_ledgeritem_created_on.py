# Generated by Django 3.1.4 on 2021-01-16 04:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210104_0554'),
    ]

    operations = [
        migrations.AddField(
            model_name='ledgeritem',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
