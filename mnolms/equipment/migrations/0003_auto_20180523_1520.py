# Generated by Django 2.0 on 2018-05-23 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0002_auto_20180523_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipment',
            old_name='equipment_type',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='equipment',
            old_name='equipment_id',
            new_name='object_id',
        ),
    ]