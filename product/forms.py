from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import CustomerInfo




PAYMENT_CHOICE = (
    ('P', 'Paystack'),
     
)

COUNTRY_CHOICE =(
    ('N', "Nigeria")
)

STATE_CHOICES =(
    ('FC, FCT'),
    ('AB, Abia'),
    ('AADB, Adamawa'),
    ('AK, Akwa Ibom'),
    ('AN, Anambra'),
    ('BA, Bauchi'),
    ('BY, Bayelsa'),
    ('BN, Benue'),
    ('BO, Borno'),
    ('CR, Cross River'),
    ('DT, Delta'),
    ('EB, Ebonyi'),
    ('ED, Edo'),
    ('EK, Ekiti'),
    ('EN, Enugu'),
    ('GB, Gombe'),
    ('IM, Imo'),
    ('JG, Jigawa'),
    ('KD, Kaduna'),
    ('KN, Kano'),
    ('KT, Katsina'),
    ('KB, Kebbi'),
    ('KG, Kogi'),
    ('KW, Kwara'),
    ('LG, Lagos'),
    ('EK, Nasarawa'),
    ('EN, Niger'),
    ('OG, Ogun'),
    ('ON, Ondo'),
    ('OS, Osun'),
    ('OY, Oyo'),
    ('PT, Plateau'),
    ('SK, Sokoto'),
    ('TA, Taraba'),
    ('YB, Yobe'),
    ('ZF, Zamfara'),
   
      


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
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Phone Number',
        'class' : 'form-control'
    }))
    # country = forms.CharField(widget=forms.Select(attrs={
    #     'placeholder': 'Select Country',
    #     'class' : 'custom-select d-block w-100'
    # }))
    # state = forms.CharField(widget=forms.SelectMultiple(attrs={
    #     'placeholder': 'Select State',
    #     'class' : 'form-control'
    # }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICE, required=True)



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