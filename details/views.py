from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template
from .forms import QuoteForm
from .models import Quote

# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')
    
def faq(request):
    return render(request, 'faq.html')


def phcn(request):
    return render(request, 'phcn.html')


def journey(request):
    return render(request, 'journey.html')


def maintenance(request):
    return render(request, 'maintenance.html')

def success(request):
    return render(request, 'contact-success.html')


def installation(request):
    return render(request, 'installation.html')


def gallery(request):
    return render(request, 'gallery.html')

def quote(request):
    form = QuoteForm(request.POST)
    context = {
        'form':form
        }
    if form.is_valid():
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        subject = form.cleaned_data.get('subject')
        address = form.cleaned_data.get('address')
        message = form.cleaned_data.get('message')
        template = get_template('quote.txt')
        content = {
            'name': name,
            "email": email,
            "phone": phone,
            'address': address,
            'subject': subject,
            'message': message

        }
        context = template.render(content)
        quote = Quote(
            name = name,
            email = email,
            phone= phone,
            address= address,
            subject= subject,
            message= message
            )
        quote.save()
        send_mail(
        'New Quote Request Form From Nakedsolar Quote Form',
        context,
        email,
        ['themajorresources@gmail.com']
        )
        
        return redirect('details:quote-success')
           
    return render(request, 'quote.html', context)


def quotesend(request):
    return render(request, 'quote-success.html')