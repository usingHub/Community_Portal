from django import forms
from .models import Request, Offer,CustomUser, Category
from django.contrib.auth.forms import UserCreationForm

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category', 'location']


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'category', 'location', 'linked_request']  # <- add this if needed

    def __init__(self, *args, **kwargs):
        linked_request = kwargs.pop('linked_request', None)
        super().__init__(*args, **kwargs)
        if linked_request:
            self.fields['linked_request'].initial = linked_request
            self.fields['linked_request'].widget = forms.HiddenInput()  # hide from user if needed


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'location', 'password1', 'password2']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']