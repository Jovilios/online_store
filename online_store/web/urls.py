from django.urls import path
from online_store.web import views
from online_store.web.views import LogoutViewCustom, LoginViewCustom, SignUpView

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginViewCustom.as_view(), name="login"),
    path("logout/", LogoutViewCustom.as_view(), name="logout"),
]