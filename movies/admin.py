from django.contrib import admin
from .models import Movie, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    search_fields = ("name",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "user", "created_at", "is_reported", "is_visible")
    list_filter = ("is_reported", "is_visible", "created_at")
    search_fields = ("content","movie__name","user__username")