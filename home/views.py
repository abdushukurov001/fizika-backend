from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import AboutModel, WhyUsModel, TypeModel, UserExperienceModel, ContactModel
from .serializer import AboutModelSerializer, WhyUsModelSerializer, TypeModelSerializer, UserExperienceModelSerializer, ContactMessageSerializer, ContactModelSerializer


@api_view(['GET'])
def about_view(request):
    about_us = AboutModel.objects.all()
    serializer = AboutModelSerializer(about_us, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def whyUs_view(request):
    why_us = WhyUsModel.objects.all()
    serializer = WhyUsModelSerializer(why_us, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def Type_view(request):
    data =  TypeModel.objects.all()
    serializer = TypeModelSerializer(data, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def UserExperience_view(request):
    data = UserExperienceModel.objects.all()
    serializer = UserExperienceModelSerializer(data, many= True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
def contactMessage_view(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Xabaringiz muvaffaqiyatli yuborildi.",
            "data": serializer.data
        }, status=201)
    return Response({
        "errors": serializer.errors
    }, status=400)


@api_view(['GET'])
def contact_view(request):
    data = ContactModel.objects.all()
    serializer = ContactModelSerializer(data, many=True)
    return Response(serializer.data, status=200)



    