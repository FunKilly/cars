import json
import urllib.request

from rest_framework import serializers

from .models import Car, Rating


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ("brand", "model")

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
        return obj.avarage_rating


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
