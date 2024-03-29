from cProfile import Profile

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .validators import validate_password_strength
from online_store.accounts.models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, validators=[validate_password_strength])
    error_messages = {
        "duplicate_email": _("A user with that email already exists."),
        "password_mismatch": _("The two password fields didn't match."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(self.error_messages["duplicate_email"], code="duplicate_email")
        return email

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Email"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Password"})


class BaseProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "phone_number", "city", "address")
        widgets = {
            # 'user': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "address": forms.Textarea(attrs={"class": "form-control", "placeholder": "Address"}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone_number) != 10:
            raise forms.ValidationError("Phone number must contain exactly 10 digits.")
        return phone_number


class ProfileEditForm(BaseProfileForm):
    pass


class ProfileDeleteForm(BaseProfileForm):
    class Meta:
        model = CustomUser
        fields = []

    def delete_user(self, commit=True):
        user_profile = self.instance

        if user_profile:
            for product in user_profile.products.all():
                for images in product.photos.all():
                    if images.image:
                        images.image.delete()

                product.photos.all().delete()

            user_profile.products.all().delete()
            user_profile.user.delete()
            user_profile.delete()

        return None



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Set initial value for user field as the email of the associated CustomUser instance
    #     if self.instance.user:
    #         self.initial['user'] = self.instance.user.email