from django.shortcuts import render
from .models import SimulatorCategory, Simulators, SimulatorType
from .serializers import SimulatorsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction

def bulk_create():
   list_bulk_create =  [
      # {
      #   'title': 'Kepler qonunlari',
      #   'description': "Kepler qonunlarini interaktiv tarzda o'rganish imkonini beradi. Planetalarning quyosh atrofida aylanishini kuzating.",
      #   'image': 'https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
      #   'link': 'https://phet.colorado.edu/sims/html/keplers-laws/latest/keplers-laws_uz.html',
      #   'types': 'Interaktiv',
      #   'categories': ['mechanics'],
      # },
      # {
      #   'title': "Ovoz To'lqinlari",
      #   'description': "Ovoz to'lqinlarining tarqalishi va xususiyatlarini o'rganish uchun simulyatsiya.",
      #   'image': 'https://images.unsplash.com/photo-1478737270239-2f02b77fc618?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
      #   'link': 'https://phet.colorado.edu/sims/html/waves-intro/latest/waves-intro_uz.html',
      #   'types': 'Interaktiv',
      #   'categories': ['waves'],
      # },
      # {
      #   'title': 'Mening Quyosh Tizimim',
      #   'description': "O'z quyosh tizimingizni yarating va gravitatsiya ta'sirida jismlarning harakatini kuzating.",
      #   'image': 'https://images.unsplash.com/photo-1614732414444-096e5f1122d5?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
      #   'link': 'https://phet.colorado.edu/sims/html/my-solar-system/latest/my-solar-system_uz.html',
      #   'types': 'Interaktiv',
      #   'categories': ['mechanics'],
      # },
      # {
      #   'title': 'Geometrik Optika: Asoslar',
      #   'description': "Linzalar va ko'zgularda nlinkarning yo'nalishini o'rganish uchun asosiy simulyatsiya.",
      #   'image': 'https://images.unsplash.com/photo-1576319155264-99536e0be1ee?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
      #   'link': 'https://phet.colorado.edu/sims/html/geometric-optics-basics/latest/geometric-optics-basics_uz.html',
      #   'types': 'Interaktiv',
      #   'categories': ['light'],
      # },
      # {
      #   'title': 'Geometrik optika',
      #   'description': "Geometrik optikaning kengaytirilgan versiyasi, murakkab optik tizimlarni o'rganish imkonini beradi.",
      #   'image': 'https://images.unsplash.com/photo-1617839647877-5df1b18be0d5?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
      #   'link': 'https://phet.colorado.edu/sims/html/geometric-optics/latest/geometric-optics_uz.html',
      #   'types': 'Interaktiv',
      #   'categories': ['light'],
      # },
      # {
      #   'title': 'Zichlik',
      #   'description': "Tlinki moddalarning zichligini o'rganish va ularning suvda cho'kishi yoki suzishini kuzatish.",
      #   'image': 'https://images.unsplash.com/photo-1527066579998-dbbae57f45ce?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
      #   'link': 'https://phet.colorado.edu/sims/html/density/latest/density_uz.html',
      #   'types': 'Interaktiv',
      #   'categories': ['mechanics'],
      # },
      # {
      #   'title': 'Elektr sxemasi: "O\'zgaruvchan tok"',
      #   'description': "O'zgaruvchan tok zanjirlarini qurish va ularning ishlashini o'rganish.",
      #   'image': 'https://images.unsplash.com/photo-1555664424-778a1e5e1b48?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
      #   'link': 'https://phet.colorado.edu/sims/html/circuit-construction-kit-ac/latest/circuit-construction-kit-ac_uz.html',
      #   'types': 'Laboratoriya',
      #   'categories': ['electricity'],
      # }
   ]
   
   for item in list_bulk_create:
        type_instance, created = SimulatorType.objects.get_or_create(name=item['types'])
        item['types'] = type_instance  
        
        categories = []
        for category_name in item['categories']:
            category_instance, created = SimulatorCategory.objects.get_or_create(name=category_name)
            categories.append(category_instance)
        item['categories'] = categories
    
   simulators = []
   for i in list_bulk_create:
        simulator = Simulators(
            title=i['title'],
            description=i['description'],
            image=i['image'],
            link=i['link'],
            types=i['types'],
        )
        simulator.save()  
        
        simulator.categories.set(i['categories'])
        simulators.append(simulator)
   

@api_view(['GET'])
def Simulators_view(request):
    # bulk_create()
    simulators = Simulators.objects.all()
    serializer = SimulatorsSerializer(simulators, many=True, context={"request": request})

    return Response(serializer.data, status=200)
