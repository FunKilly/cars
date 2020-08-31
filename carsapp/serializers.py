import json
import urllib.request

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Car, Rating


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ("brand", "model")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Car.objects.all(),
                fields=("brand", "model"),
                message=_("The specified car already exists in the system."),
            )
        ]

    def validate(self, data):
        models = self.get_models_for_make(data["brand"])

        if str(data["model"]).lower() not in models:
            raise serializers.ValidationError("Model for make hasn't been found.")
        return data

    def get_models_for_make(self, make):
        make = make.replace(" ", "_")
        url = (
            f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make}?format=json"
        )

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        response = urllib.request.urlopen(req).read()
        response = json.loads(response)

        models = [record["Model_Name"].lower() for record in response["Results"]]
        return models


class CarListSerializer(serializers.ModelSerializer):
    avarage_rating = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ("id", "brand", "model", "avarage_rating")

    def get_avarage_rating(self, obj):
        if obj.avarage_rating is None:
            return 0
        else:
            return round(obj.avarage_rating, 2)


class RatingCreateSerializer(serializers.ModelSerializer):
    car_id = serializers.UUIDField()

    class Meta:
        model = Rating
        fields = ("rate", "car_id")


class PopularCarListSerializer(serializers.ModelSerializer):
    number_of_ratings = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ["brand", "model", "number_of_ratings"]

    def get_number_of_ratings(self, obj):
        return obj.number_of_ratings
