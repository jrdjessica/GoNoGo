# Generated by Django 4.2.4 on 2023-10-04 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_attendance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='decision',
            new_name='individual_decision',
        ),
    ]