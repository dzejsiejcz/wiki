from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="title"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new_page"),
    path("edit/<str:title>", views.edit, name="edit_page"),
    path("random", views.random_page, name="random")
]
