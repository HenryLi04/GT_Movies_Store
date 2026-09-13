from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from movies.models import Movie

from .models import Order, OrderItem


@login_required
def index(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items")
    )

    template_data = {
        "title": "My Orders",
        "orders": orders,
    }

    return render(
        request,
        "orders/index.html",
        {"template_data": template_data},
    )


@login_required
@require_POST
@transaction.atomic
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(
            request,
            "Your shopping cart is empty.",
        )
        return redirect("cart.index")

    movies = Movie.objects.filter(
        id__in=cart.keys()
    )

    movies_by_id = {
        str(movie.id): movie
        for movie in movies
    }

    order_items = []
    total = Decimal("0.00")

    for movie_id, stored_quantity in cart.items():
        movie = movies_by_id.get(str(movie_id))

        if movie is None:
            continue

        try:
            quantity = int(stored_quantity)
        except (TypeError, ValueError):
            continue

        if quantity < 1:
            continue

        subtotal = movie.price * quantity
        total += subtotal

        order_items.append(
            {
                "movie": movie,
                "quantity": quantity,
            }
        )

    if not order_items:
        request.session["cart"] = {}
        request.session.modified = True

        messages.error(
            request,
            "No valid movies were found in your cart.",
        )

        return redirect("cart.index")

    order = Order.objects.create(
        user=request.user,
        total=total,
        status="completed",
    )

    OrderItem.objects.bulk_create(
        [
            OrderItem(
                order=order,
                movie=item["movie"],
                movie_name=item["movie"].name,
                unit_price=item["movie"].price,
                quantity=item["quantity"],
            )
            for item in order_items
        ]
    )

    request.session["cart"] = {}
    request.session.modified = True

    messages.success(
        request,
        f"Order #{order.id} was placed successfully.",
    )

    return redirect("orders.index")