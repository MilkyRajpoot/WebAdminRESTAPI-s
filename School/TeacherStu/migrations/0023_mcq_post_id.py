# Generated by Django 2.1.7 on 2020-07-29 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0022_auto_20200728_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='mcq_post',
            name='id',
            field=models.IntegerField(default=1),
        ),
    ]
