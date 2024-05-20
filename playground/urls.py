from django.urls import path
from . import views

# URLconf
urlpatterns = [
    path("hc/", views.hc, name="hc"),
    path("hc_restarts/", views.hc_restarts, name="hc_restarts"),
    path("hc_larger_radii/", views.hc_larger_radii, name="hc_larger_radii"),
    path("update_hc/", views.update_hc, name="update_hc"),
]