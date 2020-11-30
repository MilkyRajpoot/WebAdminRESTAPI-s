# Generated by Django 2.1.7 on 2020-09-09 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0029_auto_20200826_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteiceFire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=100)),
                ('clas', models.CharField(max_length=30)),
                ('imageLink', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='NotesFire',
        ),
    ]