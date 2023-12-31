# Generated by Django 4.2.3 on 2023-08-02 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('force', models.CharField(default='', max_length=100)),
                ('level', models.CharField(default='', max_length=100)),
                ('mechanic', models.CharField(default='', max_length=100)),
                ('equipment', models.CharField(default='', max_length=100)),
                ('primaryMuscles', models.CharField(default='', max_length=100)),
                ('secondaryMuscles', models.CharField(default='', max_length=100)),
                ('category', models.CharField(default='', max_length=100)),
                ('images', models.CharField(default='', max_length=100)),
                ('instructions', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='height_unit',
            field=models.CharField(blank=True, choices=[('cm', 'Centimeters'), ('ft', 'Feet')], default='cm', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('kg', 'Kilograms'), ('lbs', 'Pounds')], default='kg', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
