from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import EmailAuthenticationForm
from .views import (UserListView, UserDetailView, UserSkillsView,
                    UsersAddSkillsView, UsersRemoveSkillsView,
                    RegisterCreateView, CustomPasswordChangeView,
                    UserUpdateView
                    )

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            authentication_form=EmailAuthenticationForm,
        ),
        name='login'
    ),
    path('password_change/', CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('list/', UserListView.as_view()),
    path('skills/', UserSkillsView.as_view()),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('edit-profile/', UserUpdateView.as_view()),
    path('<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('<int:pk>/skills/add/', UsersAddSkillsView.as_view()),
    path('<int:pk>/skills/<int:skill_id>/remove/',
         UsersRemoveSkillsView.as_view()),
    path('', include('django.contrib.auth.urls')),

]
