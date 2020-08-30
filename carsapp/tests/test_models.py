from django.test import TestCase

from carsapp.models import Car, Rating


class CarTest(TestCase):
    def create_car(self, brand, model):
        return Car.objects.create(brand=brand, model=model)

    def test_create_car(self):
        brand = "Toyota"
        model = "Prius"

        car = self.create_car(brand, model)
        self.assertEqual(car.brand, brand)
        self.assertEqual(car.model, model)

    def test_capitalization(self):
        brand = "Toyota"
        model = "pRiUS"
        capitalized = "Prius"

        car = self.create_car(brand, model)
        self.assertEqual(car.model, capitalized)


class RatingTest(TestCase):
    def create_rating(self, car, rate):
        return Rating.objects.create(car=car, rate=rate)

    def test_create_rating(self):
        car = Car.objects.create(brand="Ford", model="Mustang")
        rate = 3

        rating = self.create_rating(car=car, rate=rate)
        self.assertEqual(rating.car, car)
        self.assertEqual(rating.rate, rate)
