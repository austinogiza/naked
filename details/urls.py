from django.urls import path, include

from . import views
app_name = 'details'


urlpatterns = [
     
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    path('faq/', views.faq, name='faq'),
  
  
    path('phcn/', views.phcn, name='phcn'),
    
    path('quote/', views.quote, name='quote'),
    path('journey/', views.journey, name='journey'),

   path('maintenance/', views.maintenance, name='maintenance'),
   path('installation/', views.installation, name='installation'),
      path('gallery/', views.gallery, name='gallery'),
   

       path('contact-success/', views.success, name='contact-success'),
        path('quote-success/', views.quotesend, name='quote-success'),
  

]
