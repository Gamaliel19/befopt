from django.views.generic import DetailView, ListView

from .models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.filter(status=Service.Status.PUBLISHED)


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"

    def get_queryset(self):
        return Service.objects.filter(status=Service.Status.PUBLISHED)
