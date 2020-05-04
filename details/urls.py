from django.urls import path, include

from . import views
app_name = 'details'


urlpatterns = [
     
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    path('faq/', views.faq, name='faq'),
  
  
    path('phcn/', views.phcn, name='phcn'),
  

]
