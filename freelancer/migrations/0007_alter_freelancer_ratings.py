# Generated by Django 4.0.1 on 2022-03-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0006_alter_freelancer_contribution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='ratings',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
