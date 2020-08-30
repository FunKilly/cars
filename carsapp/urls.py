from django.urls import path
from rest_framework import routers

from .views import CarViewSet, PopularCarView, RatingCreateView

router = routers.SimpleRouter()
router.register(r"cars", CarViewSet)

urlpatterns = [
    path("rate/", RatingCreateView.as_view(), name="rate"),
    path("popular", PopularCarView.as_view(), name="popular"),
]

urlpatterns += router.urls
