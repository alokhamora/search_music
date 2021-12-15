from django.db import models

class Track(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.artist + ' - ' + self.name
