# Generated by Django 2.1.7 on 2020-08-10 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserWeb', '0005_resultuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCQUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
