# Generated by Django 4.0.1 on 2022-02-13 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_alter_client_contribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]
