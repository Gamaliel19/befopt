from django.urls import path

from . import views

app_name = "formations"

urlpatterns = [
    path("", views.FormationListView.as_view(), name="list"),
    path("<slug:slug>/", views.FormationDetailView.as_view(), name="detail"),
]
