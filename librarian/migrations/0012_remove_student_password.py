# Generated by Django 2.2 on 2021-06-22 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0011_student_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='password',
        ),
    ]
