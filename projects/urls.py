from django.urls import path
from .views import (ProjectListView, ProjectDetailView, ProjectCompleteview,
                    ProjectParticipate, ProjectCreateView,
                    ProjectUpdateView)

app_name = 'projects'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='list'),
    path('create-project/', ProjectCreateView.as_view()),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', ProjectUpdateView.as_view(), name='update'),
    path('<int:pk>/complete/', ProjectCompleteview.as_view()),
    path('<int:pk>/toggle-participate/', ProjectParticipate.as_view()),
]
