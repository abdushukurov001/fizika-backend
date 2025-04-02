from django.shortcuts import render
from .serializers import ClassesSerializers, LessonsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Classes, Lessons, Test, TestResult, TestStatistic



class SubmitTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        test_answers = request.data.get("answers", [])  # {"test_id": selected_option}

        correct_count = 0
        total_tests = len(test_answers)
        lesson = None

        for test_id, selected_option in test_answers.items():
            try:
                test = Test.objects.get(id=test_id)
                lesson = test.resource  # Mavzuni olish
                is_correct = test.correct_option == selected_option

                # Test natijasini saqlash yoki yangilash
                test_result, created = TestResult.objects.update_or_create(
                    user=user, test=test,
                    defaults={"selected_option": selected_option, "is_correct": is_correct}
                )

                if is_correct:
                    correct_count += 1

            except Test.DoesNotExist:
                continue

        # **Test foizini saqlash yoki yangilash**
        if lesson:
            test_statistic, created = TestStatistic.objects.get_or_create(user=user, lesson=lesson)
            test_statistic.total_tests = total_tests
            test_statistic.correct_answers = correct_count
            test_statistic.update_percentage()

        return Response({
            "message": "Test natijalari saqlandi!",
            "total_tests": total_tests,
            "correct_answers": correct_count,
            "percentage": (correct_count / total_tests) * 100 if total_tests > 0 else 0
        })
    



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