from django.urls import path
from .views import (ProjectListView, ProjectDetailView, ProjectCompleteview,
                    ProjectParticipate)


urlpatterns = [
    path('list/', ProjectListView.as_view()),
    path('<int:pk>/', ProjectDetailView.as_view()),
    path('<int:pk>/complete/', ProjectCompleteview.as_view()),
    path('<int:pk>/toggle-participate/', ProjectParticipate.as_view()),
]
