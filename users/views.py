import json
from http import HTTPStatus

from common.constants import SKILL_COUNT_SHOW, USER_PAGINATE_COUNT
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from users.forms import NewUserChangeForm, RegisterForm
from users.models import Skill, User


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    ordering = ['id']
    context_object_name = 'participants'
    paginate_by = USER_PAGINATE_COUNT

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
            name__istartswith=start).order_by('name')[:SKILL_COUNT_SHOW]

        data = [{'id': skill.id, 'name': skill.name} for skill in skills]

        return JsonResponse(data, safe=False)


class UsersAddSkillsView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.id == int(self.kwargs['pk']):
            return JsonResponse({'status': 'error', 'message': 'Forbidden'},
                                status=403
                                )

        body = json.loads(request.body)
        skill_id, name = body.get('skill_id'), body.get('name')

        if skill_id is None and not name:
            return JsonResponse(
                {'status': 'error', 'message': 'Bad request'},
                status=HTTPStatus.BAD_REQUEST
            )

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
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'},
                                status=HTTPStatus.UNAUTHORIZED)

        if not request.user.id == int(self.kwargs['pk']):
            return JsonResponse({'status': 'error', 'message': 'Forbidden'},
                                status=HTTPStatus.FORBIDDEN)

        skill_id = self.kwargs['skill_id']
        if not request.user.skills.filter(pk=skill_id).exists():
            return JsonResponse({'status': 'error', 'message': 'Bad request'},
                                status=HTTPStatus.BAD_REQUEST)

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


class NewPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.pk})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = NewUserChangeForm
    template_name = 'users/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.pk})
