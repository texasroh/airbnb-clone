# Generated by Django 4.0.5 on 2022-06-13 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0010_alter_room_guests'),
        ('lists', '0003_alter_list_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='rooms',
            field=models.ManyToManyField(blank=True, related_name='list', to='rooms.room'),
        ),
    ]
