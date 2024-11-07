# import serializer from rest_framework
from rest_framework import serializers

# import model from models.py
from .models import Track

# Create a model serializer
class TrackSerializer(serializers.HyperlinkedModelSerializer):
	# specify model and fields
	class Meta:
		model = Track
		fields = ('title', 'artist')
