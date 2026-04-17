from django.urls import path
from .views import (UserListView, UserDetailView, UserSkillsView,
                    UsersAddSkillsView, UsersRemoveSkillsView)

urlpatterns = [
    path('list/', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('skills/', UserSkillsView.as_view()),
    path('<int:pk>/skills/add/', UsersAddSkillsView.as_view()),
    path('<int:pk>/skills/<int:skill_id>/remove/',
         UsersRemoveSkillsView.as_view()),

]
