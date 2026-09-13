from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def signup(request):
    if request.user.is_authenticated:
        return redirect("home.index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home.index")
    else:
        form = UserCreationForm()

    template_data = {
        "title": "Sign Up",
        "form": form,
    }

    return render(
        request,
        "accounts/signup.html",
        {"template_data": template_data},
    )