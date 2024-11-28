from django.db import models

# Create your models here.

class Track(models.Model):
	title = models.CharField(max_length=200)
	artist = models.CharField(max_length=200)
	audio_file = models.FileField(upload_to='uploads/')

	def __str__(self):
		return f"{self.id}: {self.title} - {self.artist}"
	
class Stem(models.Model):
    track = models.ForeignKey(Track, related_name="stems", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., 'vocals', 'accompaniment'
    file = models.FileField(upload_to='stems/')

    def __str__(self):
        return f"{self.name} - {self.track.title} - {self.track.artist}"

