from collections import defaultdict

from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView

from playlist_manager.models import TouristAttraction, Track
from playlist_manager.constants import ORDERING_CRITERIA_DICT
from playlist_manager.mapbox_client import MapboxClient
from playlist_manager.algorithms import dijkstra


class HomePageView(TemplateView):
    template_name = "home.html"


class AttractionListView(ListView):
    template_name = "attraction_list.html"
    paginate_by = 10
    queryset = TouristAttraction.objects.all().order_by('-selected', '-origin', '-destination')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enable_origin_selection"] = not TouristAttraction.objects.filter(origin=True).exists()
        context["enable_destination_selection"] = not TouristAttraction.objects.filter(destination=True).exists()
        return context

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

def result_view(request):
    attractions = TouristAttraction.objects.filter(selected=True)
    coords = []
    #names = []
    if attractions and attractions.count() > 1:
        for attraction in attractions:
            coords.append(
                [float(attraction.latitude), float(attraction.longitude), attraction.name]
            )

        graph = {}
        mapbox_client = MapboxClient()
        for source in coords:
            source_lat, source_lng, source_name = source
            graph[source_name] = {}
            for neighbour in coords:
                neighbour_lat, neighbour_lng, neighbour_name = neighbour

                if neighbour != source:
                    weight = mapbox_client.duration_between_coords(
                        [source_lat, source_lng],
                        [neighbour_lat, neighbour_lng]
                    )
                    graph[source_name][neighbour_name] = weight
        print(
            graph
        )
        dijkstra(graph, coords[0][2], coords[-1][2])

    return render(
        request,
        'results.html',
        {'coords':coords}
    )

class TrackListView(ListView):
    template_name = "track_list.html"
    category = None
    paginate_by = 6

    def get_queryset(self):
        if "ordering" in self.request.GET and self.request.GET["ordering"] in ["nome música", "popularidade", "duração", "artistas"]:
            ordering_criteria = self.request.GET["ordering"]
            queryset = Track.objects.all().order_by(ORDERING_CRITERIA_DICT[ordering_criteria])
            return queryset
        else:
            queryset = Track.objects.all().order_by(ORDERING_CRITERIA_DICT["popularidade"])
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordering_criteria = ["nome música", "popularidade", "duração", "artistas"]
        context["ordering_criteria"] = ordering_criteria
        if "ordering" in self.request.GET and self.request.GET["ordering"] in ["nome música", "popularidade", "duração", "artistas"]:
            context["ordering"] = self.request.GET["ordering"]
        else:
            context["ordering"] = "popularidade"
        return context
