from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response

from .mixins import GetSerializerClassMixin
from .models import Car
from .serializers import (
    CarCreateSerializer,
    CarListSerializer,
    PopularCarListSerializer,
    RatingCreateSerializer,
)


class CarViewSet(
    GetSerializerClassMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):

    queryset = Car.objects.all().with_rating()
    serializer_class = CarListSerializer
    serializer_action_classes = {
        "list": CarListSerializer,
        "create": CarCreateSerializer,
    }


class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        car = Car.objects.filter(id=serializer.validated_data.pop("car_id")).first()

        if car:
            serializer.validated_data["car"] = car
            self.perform_create(serializer)
            return Response(
                "Rating for a car has been added.", status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                "Specific car has not been found.", status=status.HTTP_400_BAD_REQUEST
            )


class PopularCarView(generics.ListAPIView):
    serializer_class = PopularCarListSerializer
    queryset = (
        Car.objects.all().with_number_of_ratings().order_by("-number_of_ratings")[:10]
    )
