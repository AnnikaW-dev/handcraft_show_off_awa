from django.urls import path
from .views import AddHandcraft, Handcrafts, HandcraftDetail


urlpatterns = [
    path("", AddHandcraft.as_view(), name="add_handcraft"),
    path("handcrafts/", Handcrafts.as_view(), name="handcrafts"),
    path("<slug:slug>/", HandcraftDetail.as_view(), name="handcraft_detail"),
]
