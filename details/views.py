from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')
    
def faq(request):
    return render(request, 'faq.html')


def phcn(request):
    return render(request, 'phcn.html')