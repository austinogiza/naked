from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import CustomerInfo




PAYMENT_CHOICE = (
    ('P', 'Paystack'),
     ('PY', 'Payu')
)

COUNTRY_CHOICE =(
    ('N', "Nigeria")
)

STATE_CHOICES =(
    ('')


)


COUNTRIES_ONLY = ['NG']

class CheckoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Full Name',
        'class' : 'form-control'
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Address',
        'class' : 'form-control'
    }))
    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Select Country',
        'class' : 'form-control'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Select State',
        'class' : 'form-control'
    }))
    
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICE, required=True)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': "Recipient's username",
        'aria-describedby': 'basic-addon2'

    }))

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'

    }), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control'

    }), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'

    }), required=True)
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'

    }), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control md-textarea',
        'resize': 'none'

    }), required=True)


class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'