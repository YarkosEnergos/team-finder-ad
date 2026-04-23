from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from projects.forms import ProjectModelForm
from projects.models import Project
from common.constants import PROJECT_PAGINATE_COUNT, STATUS_CLOSED, STATUS_OPEN


class ProjectListView(ListView):
    model = Project
    ordering = ['-created_at']
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = PROJECT_PAGINATE_COUNT

    def get_queryset(self):
        queryset = super().get_queryset(
        ).select_related('owner').prefetch_related('participants')

        return queryset


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'


class ProjectCompleteview(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))

        if request.user != project.owner:
            return JsonResponse(
                {"status": "error", "message": "Forbidden"},
                status=HTTPStatus.FORBIDDEN
            )

        if project.status != STATUS_OPEN:
            return JsonResponse(
                {"status": "error", "message": "Project already closed"},
                status=HTTPStatus.BAD_REQUEST)

        project.status = STATUS_CLOSED
        project.save()
        return JsonResponse({"status": "ok", "project_status": STATUS_CLOSED})


class ProjectParticipate(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))

        if (is_participant := project.participants.filter(
            pk=request.user.pk
        ).exists()):
            project.participants.remove(request.user)
        else:
            project.participants.add(request.user)

        return JsonResponse(
            {"status": "ok", "participant": not is_participant}
        )


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectModelForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_edit'] = False
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        self.object.participants.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectModelForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_edit'] = True
        return context

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.object.pk})
