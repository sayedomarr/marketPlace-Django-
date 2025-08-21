from django.urls import path
from .views import contact

app_name = 'contactus'

urlpatterns = [ path('contact/', contact, name='contact_us') ]
