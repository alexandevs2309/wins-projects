# Generated by Django 5.1.3 on 2024-12-15 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticacion', '0009_remove_customuser_profilepicture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]