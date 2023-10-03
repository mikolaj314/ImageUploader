from django.urls import path

from images import views


urlpatterns = [
    path("", views.ImageListCreateView.as_view(), name="image-list"),
    path(
        "expiring-links/",
        views.ExpiringLinkListCreateView.as_view(),
        name="expiring-link-create-list",
    ),
    path(
        "expiring-links/<str:signed_link>/",
        views.ExpiringLinkDetailView.as_view(),
        name="expiring-link-detail",
    ),
]
