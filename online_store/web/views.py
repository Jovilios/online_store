from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from online_store.accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from online_store.products.models import Product


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("index")
    template_name = "accounts/register.html"

    # Check if the user is authenticated and do not grant them access to the registration page.
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("index"))
        return super().dispatch(request, *args, **kwargs)

    # Automatically login user
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        user = authenticate(email=form.cleaned_data["email"], password=form.cleaned_data["password1"])

        if user is not None:
            login(self.request, user)

        return redirect(reverse('index'))


class LoginViewCustom(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "web/login.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        else:
            return reverse_lazy("index")

    # Check if the user is authenticated and do not grant them access to the login page.
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("index"))
        return super().dispatch(request, *args, **kwargs)


class LogoutViewCustom(LogoutView):
    http_method_names = ["post"]
    next_page = "/"


def index(request):
    user_profile = get_user_model()
    last_products = Product.objects.all()[:12]

    context = {
        "last_products": last_products,
        "user_profile": user_profile,
    }

    return render(request, "web/index.html", context)

