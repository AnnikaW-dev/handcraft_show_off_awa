from django.urls import path
from .views import AddHandcraft, Handcrafts, HandcraftDetail, DeleteHandcraft


urlpatterns = [
    path("add/", AddHandcraft.as_view(), name="add_handcraft"),
    path("", Handcrafts.as_view(), name="handcrafts"),
    path("<slug:slug>/", HandcraftDetail.as_view(), name="handcraft_detail"),
    path("delete/<slug:slug>/", DeleteHandcraft.as_view(), name="delete_handcraft"),
]
