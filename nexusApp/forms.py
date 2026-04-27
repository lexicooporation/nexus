from django import forms
from .models import ContactMessage
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model  = ContactMessage
        fields = ["full_name", "email", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class":"form-control","placeholder": "Full Name", "autocomplete":"name",}),
            "email": forms.EmailInput(attrs={"class":"form-control","placeholder": "Email address","autocomplete":"email",}),
            "message": forms.Textarea(attrs={"class":"form-control","placeholder": "How can we help?","rows":5,}),
            }
        labels = {"full_name": "Name", "email":"Email", "message":"Message",}


# ─── Sign-up ─────────────────────────────────────────────────────────────────

class SignUpForm(UserCreationForm):
    """
    Extends the built-in UserCreationForm with a required, unique email field.
    Email is stored in lowercase and must be unique across all accounts.
    """
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={"placeholder": "you@example.com","autocomplete": "email",}),)

    class Meta(UserCreationForm.Meta):
        model  = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# ─── Email-based login ────────────────────────────────────────────────────────

class EmailLoginForm(forms.Form):
    """
    Login form that accepts an email address instead of a username.
    Authentication is handled by nexusApp.backends.EmailBackend.
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "you@example.com","autocomplete": "email",}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Your password","autocomplete": "current-password",}),)

    def __init__(self, request=None, *args, **kwargs):
        # request is accepted so the form mirrors Django's AuthenticationForm
        # signature; it's passed through to authenticate() for middleware hooks.
        self.request    = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email    = self.cleaned_data.get("email", "").lower().strip()
        password = self.cleaned_data.get("password")

        if email and password:
            # username kwarg is used because EmailBackend receives it as email
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password. Please try again.")
            if not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache
