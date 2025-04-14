from django.urls import path
from .views import ClassesView, LessonsView, LessonsDetailView, SubmitTestView, LessonTestResultView, LessonTestResultsView


urlpatterns = [
    path('classes/', ClassesView),
    path('lessons/', LessonsView),
    path('submit-test/', SubmitTestView.as_view()),
    path('lessons/<int:id>/', LessonsDetailView),
    path('lesson-test-result/<int:lesson_id>/', LessonTestResultView.as_view()),
    path('lesson-results/', LessonTestResultsView.as_view(), name='lesson-test-results'),

]
