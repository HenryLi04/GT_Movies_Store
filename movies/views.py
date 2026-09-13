from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ReviewForm
from .models import Movie,Review


def index(request):
    search_term = request.GET.get("search", "")

    movies = Movie.objects.all()

    if search_term:
        movies = movies.filter(
            name__icontains=search_term
        )

    template_data = {
        "title": "Movies",
        "movies": movies,
        "search_term": search_term,
    }

    return render(
        request,
        "movies/index.html",
        {"template_data": template_data},
    )


def show(request, id):
    movie = get_object_or_404(Movie, id=id)

    reviews = movie.reviews.filter(
        is_visible=True
    )

    template_data = {
        "title": movie.name,
        "movie": movie,
        "reviews": reviews,
        "review_form": ReviewForm(),
    }

    return render(
        request,
        "movies/show.html",
        {"template_data": template_data},
    )


@login_required
@require_POST
def create_review(request, id):
    movie = get_object_or_404(Movie, id=id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.movie = movie
        review.user = request.user
        review.save()

        messages.success(
            request,
            "Your review was posted successfully.",
        )
    else:
        messages.error(
            request,
            "The review could not be posted.",
        )

    return redirect(
        "movies.show",
        id=movie.id,
    )

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
    )

    if request.method == "POST":
        form = ReviewForm(
            request.POST,
            instance=review,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your review was updated successfully.",
            )

            return redirect(
                "movies.show",
                id=review.movie.id,
            )
    else:
        form = ReviewForm(instance=review)

    template_data = {
        "title": "Edit Review",
        "review": review,
        "form": form,
    }

    return render(
        request,
        "movies/edit_review.html",
        {"template_data": template_data},
    )

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
    )

    if request.method == "POST":
        movie_id=review.movie.id
        review.delete()


        messages.success(
            request,
            "Your review was deleted successfully.",
        )

        return redirect(
            "movies.show",
            id=movie_id
        )

    template_data={
        "title":"Delete Review",
        "review":review,
    }

    return render(
        request,
        "movies/delete_review.html",
        {"template_data":template_data}
    )

@login_required
@require_POST
def report_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        is_visible=True,
    )

    if review.user==request.user:

        messages.error(
            request,
            "You cannot report your own review.",
        )
    else:
        review.is_reported = True
        review.is_visible = False

        review.save(
            update_fields=[
                "is_reported",
                "is_visible",
            ]
        )

        messages.success(
            request,
            "The review was reported and removed from the page.",
        )
        

    return redirect(
        "movies.show",
        id=review.movie.id,
    )