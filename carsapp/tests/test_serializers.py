from unittest.mock import patch

from django.test import TestCase

from carsapp.models import Car
from carsapp.serializers import CarCreateSerializer, CarListSerializer


def get_models_for_make(make):
    return ["mustang", "impreza", "enzo"]


class TestCarCreateSerializer(TestCase):
    @patch(
        "carsapp.serializers.CarCreateSerializer.get_models_for_make",
        side_effect=get_models_for_make,
    )
    def test_valid(self, mock):
        data = {"brand": "Ford", "model": "Enzo"}

        serializer = CarCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, data)

    @patch(
        "carsapp.serializers.CarCreateSerializer.get_models_for_make",
        side_effect=get_models_for_make,
    )
    def test_car_doesnt_exist(self, mock):
        data = {"brand": "Mercedes", "model": "Czokoloko"}

        serializer = CarCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
