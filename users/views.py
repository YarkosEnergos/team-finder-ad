import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy

from .models import User, Skill
from .forms import RegisterForm, CustomUserChangeForm


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    ordering = ['id']
    context_object_name = 'participants'

    def get_queryset(self):
        queryset = super().get_queryset()

        skill = self.request.GET.get('skill')
        if skill:
            queryset = queryset.filter(skills__name__iexact=skill)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['active_skill'] = self.request.GET.get('skill')
        context['all_skills'] = Skill.objects.all()

        return context


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'


class UserSkillsView(View):
    def get(self, request, *args, **kwargs):
        start = request.GET.get('q', '')
        skills = Skill.objects.filter(
            name__istartswith=start).order_by('name')[:10]

        data = [{'id': skill.id, 'name': skill.name} for skill in skills]

        return JsonResponse(data, safe=False)


class UsersAddSkillsView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        if not request.user.id == int(self.kwargs['pk']):
            return JsonResponse({'status': 'error', 'message': 'Forbidden'},
                                status=403)

        body = json.loads(request.body)
        skill_id, name = body.get('skill_id'), body.get('name')

        if skill_id is None and not name:
            return JsonResponse(
                {'status': 'error', 'message': 'Bad request'}, status=400)

        if skill_id is not None:
            created = False
            skill = get_object_or_404(Skill, pk=skill_id)
            if request.user.skills.filter(pk=skill_id).exists():
                added = False
            else:
                request.user.skills.add(skill)
                added = True
        else:
            skill, created = Skill.objects.get_or_create(name=name)
            skill_id = skill.id

            if request.user.skills.filter(pk=skill_id).exists():
                added = False
            else:
                request.user.skills.add(skill)
                added = True

        return JsonResponse({"skill_id": skill_id, "name": skill.name,
                             "created": created, "added": added})


class UsersRemoveSkillsView(LoginRequiredMixin, View):
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'},
                                status=401)

        if not request.user.id == int(self.kwargs['pk']):
            return JsonResponse({'status': 'error', 'message': 'Forbidden'},
                                status=403)

        skill_id = self.kwargs['skill_id']
        if not request.user.skills.filter(pk=skill_id).exists():
            return JsonResponse({'status': 'error', 'message': 'Bad request'},
                                status=400)

        request.user.skills.remove(Skill.objects.get(pk=skill_id))
        return JsonResponse({'status': 'ok'})


class RegisterCreateView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        login(self.request, user)

        return redirect(self.success_url)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    login_url = 'users:login'

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/edit_profile.html'
    login_url = 'users:login'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})
