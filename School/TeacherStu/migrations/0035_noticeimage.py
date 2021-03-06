# Generated by Django 2.1.7 on 2020-10-02 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0034_videof_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=3)),
                ('clas', models.CharField(choices=[('PREP', 'PREP'), ('LKG', 'LKG'), ('UKG', 'UKG'), ('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V'), ('VI', 'VI'), ('VII', 'VII'), ('VIII', 'VIII'), ('IX', 'IX'), ('X', 'X'), ('XI', 'XI'), ('XII', 'XII')], max_length=255)),
                ('que_Image', models.ImageField(default='images/Blank', max_length=1000, upload_to='images/NoticeImage/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
