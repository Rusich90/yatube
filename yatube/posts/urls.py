from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("group/<str:slug>/", views.group_posts, name = 'group_posts'),
]