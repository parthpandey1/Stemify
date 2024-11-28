#from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from spleeter.separator import Separator

# import local data
from .serializers import TrackSerializer, StemSerializer
from .models import Track, Stem

# create a viewset
class TrackViewSet(viewsets.ModelViewSet):
	"""
    A viewset that provides CRUD operations for the Track model.
    """
	queryset = Track.objects.all()
	serializer_class = TrackSerializer


class AddTrackView(APIView):
    """
    A custom view to handle file uploads, process stems, and save them to the database.
    """
    def post(self, request, *args, **kwargs):
        # Get data from the request
        title = request.data.get("title")
        artist = request.data.get("artist")
        audio_file = request.FILES.get("audio_file")
        
        # Validate that all fields are provided
        if not title or not artist or not audio_file:
            return Response(
                {"error": "Title, artist, and audio file are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate the file type
        if not audio_file.name.endswith(('.mp3', '.wav')):
            return Response(
                {"error": "Only .mp3 and .wav files are supported."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the Track to the database
        track = Track.objects.create(title=title, artist=artist, audio_file=audio_file)

        # Process the file using Spleeter
        try:
            separator = Separator('spleeter:2stems')
            separator.separate_to_file(audio_file.temporary_file_path(), 'output')  # Specify a path where stems are saved
            
            # Assume stems are saved as 'vocals.wav' and 'accompaniment.wav' in a folder named after the track
            stem_path = f'output/{audio_file.name.split(".")[0]}'
            vocals_path = f'{stem_path}/vocals.wav'
            accompaniment_path = f'{stem_path}/accompaniment.wav'

            # Save the stems to the database
            Stem.objects.create(track=track, name="Vocals", file=vocals_path)
            Stem.objects.create(track=track, name="Accompaniment", file=accompaniment_path)
        
        except Exception as e:
            # Handle errors during Spleeter processing
            return Response(
                {"error": f"Error processing stems: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return a success response
        return Response(
            {"message": "Track and stems created successfully."},
            status=status.HTTP_201_CREATED,
        )