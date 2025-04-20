from django.urls import path
from .views import about_view, whyUs_view, UserExperience_view, contact_view, contactMessage_view, Type_view

urlpatterns = [
   path('about/', about_view),
   path('why-us/', whyUs_view),
   path('user-experience/', UserExperience_view),
   path('contact/', contact_view),
   path('contact-message/', contactMessage_view),
   path('type/', Type_view),

]