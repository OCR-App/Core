# Generated by Django 4.2.7 on 2023-11-21 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagedata',
            name='lang',
            field=models.CharField(choices=[('none', 'None'), ('persian', 'Persian'), ('english', 'English')], default='none', max_length=7, verbose_name='Language'),
        ),
    ]
