# Generated by Django 4.0.1 on 2022-04-17 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_alter_jobs_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='experience',
        ),
    ]