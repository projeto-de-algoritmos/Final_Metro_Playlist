from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.contrib import messages


from playlist_manager.models import TouristAttraction, Track, Graph
from playlist_manager.constants import ORDERING_CRITERIA_DICT
from playlist_manager.algorithms import dijkstra, knapsack, get_selected_tracks
from playlist_manager.utils import build_graph, draw_graph, format_selected_tracks


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

    
def result_view(request):
    attractions = TouristAttraction.objects.filter(selected=True)
    origin = attractions.filter(origin=True).first()
    destination = attractions.filter(destination=True).first()

    if not origin or not destination:
        messages.add_message(
            request,
            messages.ERROR,
            'É necessário selecionar os pontos de origem e destino para visualizar os resultados'
        )
        return redirect(reverse('attraction-list'))

    if attractions and attractions.count() > 2:
        coords = []
        nodes = []
        for attraction in attractions:
            coords.append(
                [float(attraction.latitude), float(attraction.longitude), attraction.name]
            )
            nodes.append(attraction.name)

        graph_db_obj = Graph.objects.filter(
            nodes=nodes,
            origin=origin.name,
            destination=destination.name
        ).first()

        tracks = Track.objects.all().values_list('duration', 'popularity')
        tracks_durations, tracks_popularities = zip(*tracks)

        if graph_db_obj:
            capacity = int(graph_db_obj.duration) * 1000 # convert seconds to miliseconsd

            formatted_tracks = []
            formatted_tracks, tracks_total_duration = format_selected_tracks(
                capacity, tracks_durations, tracks_popularities
            )    
        else:
            graph = build_graph(coords)
            duration, shortest_path = dijkstra(graph, origin.name, destination.name)
            
            graph_db_obj = draw_graph(graph, shortest_path, nodes, origin, destination, duration)
            capacity = int(graph_db_obj.duration) * 1000 # convert seconds to miliseconsd

            formatted_tracks, tracks_total_duration = format_selected_tracks(
                capacity, tracks_durations, tracks_popularities
            )

        return render(
            request,
            'results.html',
            {
                'graph': graph_db_obj,
                'tracks': formatted_tracks,
                'tracks_total_duration': tracks_total_duration
            }
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'É necessário selecionar no mínimo 3 atrações turísticas'
        )
        return redirect(reverse('attraction-list'))

class TrackListView(ListView):
    template_name = "track_list.html"
    category = None
    paginate_by = 6

    def get_queryset(self):
        if "ordering" in self.request.GET and self.request.GET["ordering"] in [
            "nome música", "popularidade", "duração", "artistas"]:
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
        if "ordering" in self.request.GET and self.request.GET["ordering"] in [
            "nome música", "popularidade", "duração", "artistas"]:
            context["ordering"] = self.request.GET["ordering"]
        else:
            context["ordering"] = "popularidade"
        return context
