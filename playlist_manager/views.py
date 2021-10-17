from django.views.generic import TemplateView, ListView
from playlist_manager.models import TouristAttraction


class HomePageView(TemplateView):
    template_name = "home.html"


class AttractionListView(ListView):
    template_name = "attraction_list.html"
    category = None
    paginate_by = 6
    queryset = TouristAttraction.objects.all().order_by('-selected')

    #def get_queryset(self):
    #    return queryset

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    ordering_criteria = ["nome", "popularidade", "duração", "artistas"]
    #    context["ordering_criteria"] = ordering_criteria
    #    if "ordering" in self.request.GET and self.request.GET["ordering"] in ["nome", "popularidade", "duração", "artistas"]:
    #        context["ordering"] = self.request.GET["ordering"]
    #    else:
    #        context["ordering"] = "popularidade"
    #    return context
