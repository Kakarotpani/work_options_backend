# Generated by Django 4.0.1 on 2022-01-27 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Freelancer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(blank=True, max_length=30, null=True)),
                ('sex', models.CharField(max_length=6)),
                ('dob', models.DateField()),
                ('location', models.CharField(max_length=30)),
                ('qualification', models.CharField(blank=True, max_length=60, null=True)),
                ('experience', models.FloatField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='freelancerimg')),
                ('contribution', models.IntegerField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('ratings', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(blank=True, max_length=10, null=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancer.freelancer')),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancer.freelancer')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.jobs')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('subbmitted', models.BooleanField(default=False)),
                ('review', models.CharField(blank=True, max_length=100, null=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancer.freelancer')),
                ('job', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='client.jobs')),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('about', models.CharField(blank=True, max_length=30, null=True)),
                ('bid_date', models.DateTimeField(auto_now_add=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancer.freelancer')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.jobs')),
            ],
        ),
    ]
