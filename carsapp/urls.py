from django.urls import path

from .views import CarViewSet, RatingCreateApiView, PopularCarsApiView

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"cars", CarViewSet)

urlpatterns = [path("rate/", RatingCreateApiView.as_view(), name="rate"),
               path("popular", PopularCarsApiView.as_view(), name="popular")]

urlpatterns += router.urls
