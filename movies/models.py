from django.conf import settings
from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="movie_images/",
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="movie_reviews",
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_reported = models.BooleanField(
        default=False,
    )

    is_visible = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"