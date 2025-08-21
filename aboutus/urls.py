from django.urls import path
from .views import about

app_name = 'aboutus'

urlpatterns = [ path('about/', about, name='about_us') ]
