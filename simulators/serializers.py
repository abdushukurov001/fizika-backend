from .models import SimulatorCategory, SimulatorType, Simulators
from rest_framework import serializers


class SimulatorsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatorType
        fields = ['id', 'name']


class SimulatorsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatorCategory
        fields = ['id', 'name']




class SimulatorsSerializer(serializers.ModelSerializer):
    types = SimulatorsTypeSerializer( read_only=True)
    categories = SimulatorsCategorySerializer(many = True, read_only= True)

    class Meta:
        model = Simulators
        fields = ['id', 'title', 'description', 'image', 'link', 'types', 'categories']

