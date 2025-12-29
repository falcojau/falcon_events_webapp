from django import forms
from django.contrib.auth.models import User


# Form to register Users
class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]
    
    # function to save users data
    def save(self, commit=True):
        user = super().save(commit=False) # Doesnt save the user yet
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


# Form to get guest number
class JoinEventForm(forms.Form):
    guests = forms.IntegerField(
        min_value=0, 
        initial=0, 
        label="Additional Guests",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'})
    )


# Form for Contact
class ContactForm(forms.Form):
    first_name = forms.CharField(label="Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Your message", widget=forms.Textarea)