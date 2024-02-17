from django.db import models

# create tag model


class Tag(models.Model):
    label = models.CharField(max_length=255)
