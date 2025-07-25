# Generated by Django 5.1.6 on 2025-07-26 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0003_alter_administrator_gender_alter_administrator_role'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this admin belongs to.', related_name='administrator_set', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='administrator',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this admin.', related_name='administrator_permissions_set', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
