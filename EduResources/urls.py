from django.urls import path
from .views import ClassesView, LessonsView, LessonsDetailView, SubmitTestView


urlpatterns = [
    path('classes/', ClassesView),
    path('lessons/', LessonsView),
    path('submit-test/', SubmitTestView.as_view()),
    path('lessons/<int:id>/', LessonsDetailView),

]
