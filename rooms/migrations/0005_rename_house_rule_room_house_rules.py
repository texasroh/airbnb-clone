# Generated by Django 4.0.4 on 2022-05-16 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_alter_amenity_options_alter_facility_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='house_rule',
            new_name='house_rules',
        ),
    ]
