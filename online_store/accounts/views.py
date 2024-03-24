from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from online_store.accounts.forms import ProfileEditForm, ProfileDeleteForm
from online_store.accounts.models import UserProfile


@login_required
def profile_edit(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)

    if request.user != user_profile.user:
        return render(request, "web/error_page.html",
                      {"error_message": "You do not have permission to edit this profile."})

    form = ProfileEditForm(request.POST or None, instance=user_profile)

    if form.is_valid():
        form.save()
        return redirect("profile_details", pk=pk)

    context = {
        "user_profile": user_profile,
        "pk": pk,
        "form": form
    }
    return render(request, "accounts/profile_edit.html", context)


@login_required
def profile_details(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    products = user_profile.products.all()

    if user_profile.user != request.user:
        return render(request, "web/error_page.html", {"error_message": "Unauthorized access"})

    context = {
        "user_profile": user_profile,
        "products": products
    }

    return render(request, "accounts/profile_details.html", context)


@login_required
def profile_delete(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)

    if user_profile.user != request.user:
        return render(request, "web/error_page.html", {"error_message": "Unauthorized access"})

    form = ProfileDeleteForm(request.POST or None, instance=user_profile)

    if form.is_valid():
        form.delete_user()
        return redirect("index")

    context = {
        "user_profile": user_profile,
        "form": form
    }

    return render(request, "accounts/profile_delete.html", context)