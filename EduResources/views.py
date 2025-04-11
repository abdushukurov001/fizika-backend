from django.shortcuts import render
from .serializers import ClassesSerializers, LessonsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Classes, Lessons, Test, TestResult, TestStatistic
from rest_framework import status


class SubmitTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        test_answers = request.data.get("answers", {})
        lesson_id = request.data.get("lesson")
        
        if not lesson_id:
            return Response({
                "detail": "Dars ID (lesson) ko'rsatilmagan."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user has already taken this specific lesson's test
        if TestStatistic.objects.filter(user=user, lesson_id=lesson_id).exists():
            return Response({
                "detail": "Siz bu dars testini allaqachon topshirgansiz."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        correct_count = 0
        total_tests = len(test_answers)
        lesson = None
        
        for test_id, selected_option in test_answers.items():
            try:
                test_id = int(test_id)  # Ensure test_id is an integer
                test = Test.objects.get(id=test_id)
                
                # Verify this test belongs to the specified lesson
                if test.resource.id != int(lesson_id):
                    continue
                    
                lesson = test.resource
                is_correct = test.correct_option == selected_option
                
                # Create test result
                TestResult.objects.create(
                    user=user,
                    test=test,
                    selected_option=selected_option,
                    is_correct=is_correct
                )
                
                if is_correct:
                    correct_count += 1
                    
            except Test.DoesNotExist:
                continue
            except ValueError:
                continue
        
        # Save statistics
        if lesson:
            test_statistic, created = TestStatistic.objects.get_or_create(
                user=user, lesson=lesson
            )
            test_statistic.total_tests = total_tests
            test_statistic.correct_answers = correct_count
            test_statistic.update_percentage()
            test_statistic.save()
            
            percentage = (correct_count / total_tests) * 100 if total_tests > 0 else 0
            
            return Response({
                "message": "Test natijalari saqlandi!",
                "total_tests": total_tests,
                "correct_answers": correct_count,
                "percentage": percentage
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "Dars topilmadi yoki test javoblari noto'g'ri formatda."
            }, status=status.HTTP_400_BAD_REQUEST)


class LessonTestResultView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, lesson_id):
        user = request.user
        try:
            stat = TestStatistic.objects.get(user=user, lesson_id=lesson_id)
            return Response({
                "percentage": stat.percentage,
                "correct_answers": stat.correct_answers,
                "total_tests": stat.total_tests
            }, status=status.HTTP_200_OK)
        except TestStatistic.DoesNotExist:
            return Response({
                "detail": "Siz hali bu dars uchun test ishlamagansiz."
            }, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def ClassesView(request):
    classes = Classes.objects.all()
    serializer = ClassesSerializers(classes, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def LessonsView(request):
    lessons = Lessons.objects.all()
    serializer = LessonsSerializer(lessons,many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def LessonsDetailView(request, id):
    lesson = Lessons.objects.filter(id=id).first()
    if lesson is None:
        return Response({"detail": "Not found."}, status=404) 
    serializer = LessonsSerializer(lesson)
    return Response(serializer.data, status=200)