# Generated by Django 2.1.7 on 2020-07-23 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0008_auto_20200723_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]