# Generated by Django 4.0.4 on 2022-05-16 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_rename_house_rule_room_house_rules'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='bath',
            new_name='baths',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='bedroom',
            new_name='bedrooms',
        ),
    ]
