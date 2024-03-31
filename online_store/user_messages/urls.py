from django.urls import path

from online_store.user_messages.views import inbox, respond_to_message

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('respond_to_message/<int:message_id>/', respond_to_message, name='respond_to_message'),
]