from django.db import models
from django.utils import timezone

from crawlers.spiders.movies import ClickTheCitySpider


class Cinema(models.Model):
    name = models.CharField(max_length=64)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def fetch(self):
        spider = ClickTheCitySpider(self.url)
        results = spider.crawl()
        for room in results:
            if not room['movies']:
                continue

            movie, created = Movie.objects.get_or_create(
                cinema=self,
                room=room['room'],
                created_at__date=timezone.now()
            )

            for m in room['movies']:
                movie.title = m['title']
                movie.price = m['price']
                movie.genre = m['genre']
                movie.running_time = m['running_time']
                movie.schedule = ", ".join(m['schedule'])
            movie.save()


class Movie(models.Model):
    cinema = models.ForeignKey(Cinema, null=True, on_delete=models.CASCADE)
    room = models.CharField(max_length=64)

    title = models.CharField(max_length=255)
    price = models.CharField(max_length=16)
    genre = models.CharField(max_length=64)
    running_time = models.CharField(max_length=16)
    schedule = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
