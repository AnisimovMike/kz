from django.urls import path
from KZ import views

urlpatterns = [
    path("", views.index),
    path("about", views.about),
    path("get_list", views.get_list),
    path("get_obj/<str:n>/<str:obj_id>", views.obj),
    path("graphics/<str:graphics_id>", views.graphics),
]
