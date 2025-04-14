from rest_framework import serializers
from .models import Lessons, Test, TestResult, Classes, TestStatistic


class TestResultSerializer(serializers.ModelSerializer):
    correct_option  = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'selected_option', 'is_correct', 'created_at', 'correct_option']

    def get_correct_option(self, obj):
        return obj.test.correct_option


class TestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Test
        fields = ['id', 'question', 'option1', 'option2', 'option3', 'option4', 'correct_option']

class TestStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStatistic
        fields = ['percentage', 'correct_answers', 'total_tests']



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
