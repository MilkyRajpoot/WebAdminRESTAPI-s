# Generated by Django 2.1.7 on 2020-07-23 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0005_auto_20200723_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='user_code',
            field=models.CharField(max_length=100),
        ),
    ]
