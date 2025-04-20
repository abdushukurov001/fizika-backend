from rest_framework import serializers
from .models import (
    AboutModel,
    WhyUsModel,
    TypeModel,
    UserExperienceModel,
    ContactModel,
    SocialMedia,
    ContactMessage
)

class AboutModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutModel
        fields = '__all__'


class WhyUsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyUsModel
        fields = '__all__'


class TypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeModel
        fields = '__all__'


class UserExperienceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperienceModel
        fields = '__all__'


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'


class ContactModelSerializer(serializers.ModelSerializer):
    socials = SocialMediaSerializer(many=True, read_only=True)

    class Meta:
        model = ContactModel
        fields = '__all__'


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
