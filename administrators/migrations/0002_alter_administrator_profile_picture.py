# Generated by Django 5.1.6 on 2025-07-25 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='admin_profiles/'),
        ),
    ]
