# Generated by Django 4.0.1 on 2022-05-05 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0007_alter_freelancer_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='about',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
