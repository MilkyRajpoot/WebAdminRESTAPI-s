# Generated by Django 2.1.7 on 2020-10-03 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0036_auto_20201002_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticeimage',
            name='clas',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
