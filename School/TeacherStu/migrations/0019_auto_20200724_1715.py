# Generated by Django 2.1.7 on 2020-07-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0018_auto_20200724_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcq_question',
            name='flag',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='mcq_question',
            name='que_Image',
            field=models.ImageField(default='Blank', max_length=1000, upload_to='images/'),
        ),
    ]