# Generated by Django 2.1.7 on 2020-07-23 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0003_auto_20200723_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='studentClas',
        ),
    ]
