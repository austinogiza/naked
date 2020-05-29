from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import CustomerInfo




PAYMENT_CHOICE = (
    ('P', 'Paystack'),
     
)
COUNTRY_CHOICE =(
    ('CN','Select Country'),    
    ('Nigeria', "Nigeria"),
)

STATE_CHOICES =(
    ('Abuja', 'FCT'),
    ('Abia', 'Abia'),
    ('Adamawa','Adamawa'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
   
      


)
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
    country = forms.ChoiceField(widget=forms.Select, choices=COUNTRY_CHOICE)
    state = forms.ChoiceField(widget=forms.Select, choices=STATE_CHOICES)
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    # payment_option = forms.ChoiceField(
    #     widget=forms.RadioSelect, choices=PAYMENT_CHOICE, required=True)



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


class CallForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'

    }), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control'

    }), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'

    }), required=True)
    



class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'