from django.db import models

class CarQuerySet(models.QuerySet):
    def with_rating(self):
        return self.annotate(avarage_rating=models.Avg("rating__rate"))

    def with_number_of_ratings(self):
        return self.annotate(number_of_ratings=models.Count("rating"))

class CarManager(models.Manager.from_queryset(CarQuerySet)):
    use_in_migrations = True