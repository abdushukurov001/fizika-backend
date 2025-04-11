from django.urls import path
from .views import Simulators_view


urlpatterns = [
   path('simulators/', Simulators_view)

]
