from rest_framework import serializers
from .models import Lessons, Test, TestResult, Classes


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'answers', 'score', 'total_score', 'percentage']


class TestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Test
        fields = ['id', 'question', 'option1', 'option2', 'option3', 'option4', 'correct_option']



class LessonsSerializer(serializers.ModelSerializer):
    tests =  TestSerializer(many=True, read_only=True) 

    class Meta:
        model = Lessons
        fields = ['id', 'lesson', 'classes', 'title', 'description', 'videoUrl', 'tests']



class ClassesSerializers(serializers.ModelSerializer):
    lessons = LessonsSerializer(many=True, read_only=True)

    class Meta:
        model = Classes
        fields = ['id', 'name', 'lessons']
