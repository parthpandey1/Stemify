from rest_framework import serializers
from .models import Track, Stem

class StemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stem
        fields = ('name', 'file')
        
class TrackSerializer(serializers.ModelSerializer):
	stems = StemSerializer(many=True, read_only=True)
	
	class Meta:
		model = Track
		fields = ('title', 'artist', 'audio_file', 'stems')
            