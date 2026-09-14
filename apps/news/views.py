from django.views.generic import DetailView, ListView

from .models import NewsArticle


class NewsListView(ListView):
    model = NewsArticle
    template_name = "news/list.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        return NewsArticle.objects.filter(status=NewsArticle.Status.PUBLISHED)


class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = "news/detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return NewsArticle.objects.filter(status=NewsArticle.Status.PUBLISHED)
