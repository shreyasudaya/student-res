# Generated by Django 4.2.2 on 2023-06-25 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentres', '0006_rename_notes_review_note'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='note',
            new_name='notes',
        ),
    ]
