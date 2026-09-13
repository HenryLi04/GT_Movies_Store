from django.shortcuts import render,get_object_or_404,redirect
from decimal import Decimal
from django.contrib import messages
from django.views.decorators.http import require_POST
from movies.models import Movie

def index(request):
    cart = request.session.get("cart",{})

    movie_ids = cart.keys()
    movies = Movie.objects.filter(id__in=movie_ids)

    cart_items = []
    total = Decimal("0.00")

    for movie in movies:
        quantity = cart.get(str(movie.id),0)
        subtotal = movie.price*quantity
        total += subtotal

        cart_items.append(
            {
                "movie":movie,
                "quantity":quantity,
                "subtotal":subtotal,
            }
        )

    template_data = {
        "title":"Shopping Cart",
        "cart_items":cart_items,
        "total":total,
    }

    return render(
        request,
        "cart/index.html",
        {"template_data": template_data},
    )

@require_POST
def add(request, id):
    movie = get_object_or_404(Movie, id=id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if quantity > 99:
        quantity = 99

    cart = request.session.get("cart", {})
    movie_id = str(movie.id)

    current_quantity = cart.get(movie_id, 0)
    cart[movie_id] = min(
        current_quantity + quantity,
        99,
    )

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(
        request,
        f"{movie.name} was added to your cart.",
    )

    return redirect(
        "movies.show",
        id=movie.id,
    )

@require_POST
def remove(request,id):
    movie = get_object_or_404(Movie,id=id)

    cart = request.session.get("cart",{})
    movie_id = str(movie.id)

    if movie_id in cart:
        del cart[movie_id]

        request.session["cart"]=cart
        request.session.modified = True

        messages.success(
            request,
            f"{movie.name} was removed from your cart."
        )

    return redirect("cart.index")


@require_POST
def clear(request):
    request.session["cart"] = {}
    request.session.modified = True

    messages.success(
        request,
        "Your shopping cart was cleared.",
    )

    return redirect("cart.index")


