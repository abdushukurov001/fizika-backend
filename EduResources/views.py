from django.shortcuts import render
from .serializers import ClassesSerializers, LessonsSerializer,TestResultSerializer, TestStatisticSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Classes, Lessons, Test, TestResult, TestStatistic
from rest_framework import status, generics




class LessonTestResultsView(generics.ListAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TestResult.objects.all()
        lesson_id = self.request.query_params.get('lesson_id')

        if lesson_id:
            queryset = queryset.filter(test__resource__id=lesson_id, user=self.request.user)

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({
                "detail": "Siz hali bu dars uchun test ishlamagansiz."
            }, status=status.HTTP_200_OK)
            
        # Calculate overall statistics
        lesson_id = self.request.query_params.get('lesson_id')
        try:
            stat = TestStatistic.objects.get(user=request.user, lesson_id=lesson_id)
            serializer = TestStatisticSerializer(stat)
            
            # Get all answers for this lesson
            test_results = queryset.select_related('test')
            answers = {result.test.id: result.selected_option for result in test_results}
            
            response_data = serializer.data
            response_data['answers'] = answers
            
            return Response(response_data)
        except TestStatistic.DoesNotExist:
            return Response({
                "detail": "Siz hali bu dars uchun test ishlamagansiz."
            }, status=status.HTTP_200_OK)
    
class LessonTestResultView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, lesson_id):
        user = request.user
        try:
            stat = TestStatistic.objects.get(user=user, lesson_id=lesson_id)
            
            # Get all answers for this lesson
            test_results = TestResult.objects.filter(
                user=user,
                test__resource_id=lesson_id
            ).select_related('test')
            
            answers = {result.test.id: result.selected_option for result in test_results}
            
            return Response({
                "percentage": stat.percentage,
                "correct_answers": stat.correct_answers,
                "total_tests": stat.total_tests,
                "answers": answers
            }, status=status.HTTP_200_OK)
        except TestStatistic.DoesNotExist:
            return Response({
                "detail": "Siz hali bu dars uchun test ishlamagansiz."
            }, status=status.HTTP_200_OK)

class SubmitTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        lesson_id = request.data.get('lesson')
        answers = request.data.get('answers', {})
        
        if not lesson_id:
            return Response({"detail": "Dars ID si ko'rsatilmagan"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            lesson = Lessons.objects.get(id=lesson_id)
        except Lessons.DoesNotExist:
            return Response({"detail": "Dars topilmadi"}, status=status.HTTP_404_NOT_FOUND)
            
        # Delete existing results for this lesson if any
        TestResult.objects.filter(
            user=request.user,
            test__resource_id=lesson_id
        ).delete()
        
        # Save new results
        for test_id, selected_option in answers.items():
            try:
                test = Test.objects.get(id=test_id, resource=lesson)
                TestResult.objects.create(
                    user=request.user,
                    test=test,
                    selected_option=selected_option
                )
            except Test.DoesNotExist:
                continue  # Skip invalid test IDs
        
        # Get the updated statistics
        try:
            stat = TestStatistic.objects.get(user=request.user, lesson=lesson)
            return Response({
                "percentage": stat.percentage,
                "correct_answers": stat.correct_answers,
                "total_tests": stat.total_tests
            }, status=status.HTTP_200_OK)
        except TestStatistic.DoesNotExist:
            return Response({"detail": "Xatolik yuz berdi"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        
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