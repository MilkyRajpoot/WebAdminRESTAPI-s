# Generated by Django 2.1.7 on 2020-08-26 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0028_auto_20200826_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notesfire',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
