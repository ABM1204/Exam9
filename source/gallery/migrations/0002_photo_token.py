# Generated by Django 5.1 on 2024-08-31 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='token',
            field=models.CharField(blank=True, max_length=36, null=True, unique=True),
        ),
    ]
