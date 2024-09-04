from django.urls import path

from . import views

app_name = "entries"

urlpatterns = [
    path("entries/", views.entry_list, name="entry_list"),
    path("entries/create/", views.entry_create, name="entry_create"),
    path("entries/<int:pk>/", views.entry_detail, name="entry_detail"),
    path("entries/<int:pk>/update/", views.entry_update, name="entry_update"),
    path("entries/<int:pk>/delete/", views.entry_delete, name="entry_delete"),
]
