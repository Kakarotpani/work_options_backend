# Generated by Django 4.0.1 on 2022-04-18 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_remove_client_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_skills',
            name='skill',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
