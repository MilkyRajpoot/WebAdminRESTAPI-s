# Generated by Django 2.1.7 on 2020-07-23 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0002_auto_20200723_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studata',
            name='studentClas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='TeacherStu.StuClas'),
        ),
    ]
