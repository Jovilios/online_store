from django.urls import path
from online_store.accounts.views import profile_edit, profile_details, profile_delete, change_password

urlpatterns = [
    path("edit/<int:pk>/", profile_edit, name="profile_edit"),
    path("details/<int:pk>/", profile_details, name="profile_details"),
    path("delete/<int:pk>/", profile_delete, name="profile_delete"),
    path("change-password/<int:pk>/", change_password, name="change_password"),


]