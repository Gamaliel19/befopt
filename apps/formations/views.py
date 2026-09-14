from django.views.generic import DetailView, ListView

from .models import Formation


class FormationListView(ListView):
    model = Formation
    template_name = "formations/list.html"
    context_object_name = "formations"
    paginate_by = 9

    def get_queryset(self):
        return Formation.objects.filter(status=Formation.Status.PUBLISHED)


class FormationDetailView(DetailView):
    model = Formation
    template_name = "formations/detail.html"
    context_object_name = "formation"

    def get_queryset(self):
        return Formation.objects.filter(status=Formation.Status.PUBLISHED)
