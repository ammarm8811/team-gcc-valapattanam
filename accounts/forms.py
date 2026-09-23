from django import forms
from .models import User
import re
from datetime import date
from django.contrib.auth.password_validation import validate_password

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[validate_password]
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'phone_whatsapp',
            'dob',
            'blood_group',
        ]

    def clean_phone_whatsapp(self):

        phone = self.cleaned_data.get('phone_whatsapp')

        if not re.match(r'^\+?[0-9]{8,15}$', phone):
            raise forms.ValidationError(
                "Enter a valid WhatsApp number."
            )

        return phone


    def clean_dob(self):

        dob = self.cleaned_data.get('dob')

        if dob and dob > date.today():
            raise forms.ValidationError(
                "Date of birth cannot be in the future."
            )

        return dob


    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data

class LoginForm(forms.Form):

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )