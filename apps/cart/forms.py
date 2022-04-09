from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    location = forms.CharField(max_length=255)
    code = forms.CharField(max_length=10)
    