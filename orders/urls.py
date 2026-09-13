from django.urls import path
from . import views
urlpatterns = [
    path(
        "",
        views.index,
        name="orders.index",
    ),

    path(
        "checkout/",
        views.checkout,
        name="orders.checkout",
    ),
]