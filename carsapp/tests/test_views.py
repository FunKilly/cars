from random import randint
from statistics import mean
from unittest.mock import patch
from uuid import uuid4

from django.test import TestCase
from django.urls import reverse

from carsapp.models import Car, Rating


class TestCarViewSet(TestCase):
    def test_get(self):
        car = Car.objects.create(brand="Ford", model="Mustang")
        rates = [2, 4, 4]
        for rate in rates:
            Rating.objects.create(car=car, rate=rate)

        response = self.client.get(reverse("car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], str(car.id))
        self.assertEqual(response.data[0]["avarage_rating"], mean(rates))

    @patch(
        "carsapp.serializers.CarCreateSerializer.get_models_for_make",
        return_value=["mustang", "escape", "explorer"],
    )
    def test_post(self, mock):
        data = {"brand": "Ford", "model": "Mustang"}

        response = self.client.post(reverse("car-list"), data=data)

        self.assertEqual(response.status_code, 201)

        car_exists = Car.objects.filter(brand=data["brand"], model=data["model"]).exists()

        self.assertTrue(car_exists)

    @patch(
        "carsapp.serializers.CarCreateSerializer.get_models_for_make",
        return_value=["mustang", "escape", "explorer"],
    )
    def test_car_does_not_exist(self, mock):
        data = {"brand": "Ford", "model": "Panamera"}

        response = self.client.post(reverse("car-list"), data=data)

        self.assertEqual(response.status_code, 400)

        car_exists = Car.objects.filter(brand=data["brand"], model=data["model"]).exists()
        self.assertFalse(car_exists)


class TestRatingCreateView(TestCase):
    def test_create(self):
        car = Car.objects.create(brand="Ferrari", model="Enzo")
        rate = 4

        data = {"car_id": car.id, "rate": rate}

        response = self.client.post(reverse("rate"), data=data)

        self.assertEqual(response.status_code, 201)

        rating_exists = Rating.objects.filter(car=car, rate=rate).exists()

        self.assertTrue(rating_exists)

    def test_car_does_not_exist(self):
        id = uuid4()

        data = {"car_id": id, "rate": "4"}

        response = self.client.post(reverse("rate"), data=data)

        self.assertEqual(response.status_code, 400)


class TestPopularCarView(TestCase):
    def test_get_top_popular_cars(self):
        for i in range(10):
            car = Car.objects.create()

        rated_cars = [
            Car.objects.create(brand="Ferrari", model=randint(1, 1000)) for i in range(10)
        ]
        cars = [
            Car.objects.create(brand="Ford", model=randint(1, 1000)) for i in range(10)
        ]

        for car in rated_cars:
            [
                Rating.objects.create(car=car, rate=randint(0, 5))
                for i in range(randint(1, 8))
            ]

        response = self.client.get(reverse("popular"))

        response_cars = {(record["brand"], record["model"]) for record in response.data}
        rated_cars_set = {(car.brand, str(car.model)) for car in rated_cars}

        self.assertTrue(response_cars.issubset(rated_cars_set))
        self.assertEqual(len(response_cars), len(rated_cars_set))
