from playlist_manager.models import TouristAttraction
from django.shortcuts import redirect


def remove_attraction(request, pk):
    attraction = TouristAttraction.objects.get(pk=pk)
    attraction.selected = False
    attraction.save()
    return redirect('/attractions')


def select_attraction(request, pk):
    attraction = TouristAttraction.objects.get(pk=pk)
    attraction.selected = True
    attraction.save()
    return redirect('/attractions')

def select_attraction_origin(request, pk):
    attraction = TouristAttraction.objects.get(pk=pk)
    attraction.origin = True
    attraction.save()
    return redirect('/attractions')

def remove_attraction_origin(request, pk):
    attraction = TouristAttraction.objects.get(pk=pk)
    attraction.origin = False
    attraction.save()
    return redirect('/attractions')

def select_attraction_destination(request, pk):
    attraction = TouristAttraction.objects.get(pk=pk)
    attraction.destination = True
    attraction.save()
    return redirect('/attractions')

def remove_attraction_destination(request, pk):
    attraction = TouristAttraction.objects.get(pk=pk)
    attraction.destination = False
    attraction.save()
    return redirect('/attractions')