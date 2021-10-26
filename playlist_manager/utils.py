import io
from datetime import datetime

import networkx as nx
import matplotlib.pyplot as plt

from django.core.files.images import ImageFile

from playlist_manager.mapbox_client import MapboxClient
from playlist_manager.models import Graph, TouristAttraction, Track
from playlist_manager.algorithms import knapsack, get_selected_tracks


def build_graph(coords: list):
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

    return graph


def chunks(l, n):
    n = max(1, n)
    return list((set(l[i:i+n]) for i in range(0, len(l), n)))


def draw_graph(graph: dict, shortest_path: list,
               nodes: list, origin: TouristAttraction,
               destination: TouristAttraction,
               duration: int):

    graph_nx_format = {}

    for node in graph:
        graph_nx_format[node] = {}
        for neighbour in graph[node]:
            graph_nx_format[node][neighbour] = {'weight': graph[node][neighbour]}

    nx_graph = nx.from_dict_of_dicts(graph_nx_format)

    pos = nx.spring_layout(nx_graph)
    labels = nx.get_edge_attributes(nx_graph, 'weight')

    shortest_path_chunks = chunks(shortest_path, 2)
    edge_colors = ['red' if set(edge) in shortest_path_chunks else 'black' for edge in nx_graph.edges]

    plt.figure(figsize=(7, 5,)) # Size in inches
    nx.draw_networkx(
        nx_graph,
        pos,
        node_size=[len(graph[node])*300 for node in graph],
        font_size=6,
        edge_color=edge_colors
    )
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=labels, font_size=6)

    figure = io.BytesIO()

    plt.savefig(figure, format="png")

    file_content = ImageFile(figure)
    graph_db = Graph(
        nodes = nodes,
        origin = origin.name,
        destination = destination.name,
        path=shortest_path,
        duration=duration
    )
    graph_db.image.save('graph.png', file_content)
    graph_db.save()

    return graph_db


def format_selected_tracks(capacity, tracks_durations, tracks_popularities):
    playlist_items = knapsack(capacity, tracks_durations, tracks_popularities)
    selected_tracks = get_selected_tracks(playlist_items, tracks_durations, capacity)

    formatted_tracks = []
    tracks_total_duration = 0

    for track_duration in selected_tracks:
        track = Track.objects.filter(duration=track_duration).first()
        formatted_tracks.append(
            {
                'name': track.name,
                'duration': track.duration_formatted,
                'popularity': track.popularity
            }
        )
        tracks_total_duration += track.duration

    parsed_duration = datetime.fromtimestamp(tracks_total_duration/1000)
    minutes = parsed_duration.minute
    seconds = f"0{parsed_duration.second}" if parsed_duration.second / 10 < 1 else parsed_duration.second

    return formatted_tracks, f"{minutes}:{seconds}"
