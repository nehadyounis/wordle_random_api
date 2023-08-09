from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=30, unique=True, primary_key=True)
    length = models.IntegerField(default=0)
    frequency = models.IntegerField(default=0)
    type = models.CharField(max_length=10, default=None)
    language = models.CharField(max_length=2, default='en')
    is_common = models.BooleanField(default=False)
    n_of_times = models.IntegerField(default=0)

    def __str__(self):
        return str(self.word) + " - " + str(self.type)


class RateLimiter(models.Model):
    ip = models.CharField(max_length=16)
    country_code = models.CharField(max_length=3, default=None)
    counter = models.IntegerField(default=0)
    last_request_timestamp = models.IntegerField(default=0)


class Statistic(models.Model):
    key = models.CharField(max_length=20)
    value = models.IntegerField(default=0)
