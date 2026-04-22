from django.contrib.auth import views as auth_views
from django.urls import include, path
from users.forms import EmailAuthenticationForm
from users.views import (NewPasswordChangeView, RegisterCreateView,
                         UserDetailView, UserListView, UsersAddSkillsView,
                         UserSkillsView, UsersRemoveSkillsView, UserUpdateView)

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            authentication_form=EmailAuthenticationForm,
        ),
        name='login'
    ),
    path('password_change/', NewPasswordChangeView.as_view(),
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
