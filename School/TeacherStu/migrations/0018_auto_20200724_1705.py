# Generated by Django 2.1.7 on 2020-07-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0017_auto_20200724_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcq_question',
            name='que_Image',
            field=models.ImageField(blank=True, default='None', max_length=1000, null=True, upload_to='images/'),
        ),
    ]
