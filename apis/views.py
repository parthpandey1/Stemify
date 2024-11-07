from django.shortcuts import render

# Create your views here.

# import viewsets
from rest_framework import viewsets

# import local data
from .serializers import TrackSerializer
from .models import Track

# create a viewset


class TrackViewSet(viewsets.ModelViewSet):
	# define queryset
	queryset = Track.objects.all()

	# specify serializer to be used
	serializer_class = TrackSerializer
