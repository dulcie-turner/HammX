# Generated by Django 3.1 on 2022-11-20 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=200)),
                ('regionLon', models.FloatField()),
                ('regionLat', models.FloatField()),
                ('photoperiod', models.CharField(max_length=200)),
                ('soilTexture', models.CharField(max_length=200)),
                ('soilFertility', models.CharField(max_length=200)),
                ('soilPh', models.FloatField()),
                ('resToChange', models.FloatField()),
                ('optPreference', models.FloatField()),
                ('timescale', models.CharField(max_length=200)),
                ('scalePreference', models.FloatField()),
                ('cropCat', models.TextField()),
                ('nutrientCat', models.TextField()),
                ('currentCrops', models.TextField()),
            ],
        ),
    ]
