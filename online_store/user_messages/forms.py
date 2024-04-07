from django import forms
from online_store.user_messages.models import Message


class BaseMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body"]


class MessageForm(BaseMessageForm):
    class Meta:
        model = Message
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control", "placeholder": "Message to seller"}),
        }
        labels = {
            "body": "",
        }


class MessageRespondForm(BaseMessageForm):
    class Meta:
        model = Message
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control", "placeholder": "Replay"}),
        }
        labels = {
            "body": "",
        }
