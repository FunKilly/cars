from statistics import mean

from django.test import TestCase

from carsapp.models import Car, Rating


class CarManagerTest(TestCase):
    def setUp(self):
        car = Car.objects.create(brand="Ford", model="Mustang")

        self.rates = [4, 2, 1]
        for rate in self.rates:
            Rating.objects.create(car=car, rate=rate)
        self.avg_rate = mean(self.rates)

    def test_with_rating(self):
        queryset = Car.objects.all().with_rating()

        self.assertEqual(queryset[0].avarage_rating, self.avg_rate)

    def test_with_number_of_ratings(self):
        queryset = Car.objects.all().with_number_of_ratings()

        self.assertEqual(queryset[0].number_of_ratings, len(self.rates))
