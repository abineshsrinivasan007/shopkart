# Generated by Django 4.2.7 on 2024-11-23 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_favourite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favourite',
            old_name='Product',
            new_name='product',
        ),
    ]
