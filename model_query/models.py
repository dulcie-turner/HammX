from django.db import models

# Create your models here.

class ModelInput(models.Model):
    # region
        # region, (region to lon lat), photoperiod

    # soil
        # texture, fertility, ph

    # model
        # resistance to change, optimal vs absolute, timescale

    # crop
        # large scale preference, crop cat, nutrient groups

    region = models.CharField(max_length=200)
    regionLon = models.FloatField()
    regionLat = models.FloatField()
    photoperiod = models.CharField(max_length=200)

    soilTexture = models.CharField(max_length=200)
    soilFertility = models.CharField(max_length=200)
    soilPh = models.FloatField()

    resToChange = models.FloatField()
    optPreference = models.FloatField()
    timescale = models.CharField(max_length=200)

    scalePreference = models.FloatField()
    cropCat = models.TextField() # written as a CSV list - django has no list field
    nutrientCat = models.TextField()
    currentCrops = models.TextField()
    