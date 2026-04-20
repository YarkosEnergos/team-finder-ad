from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from projects.models import Project
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy

from .forms import ProjectModelForm


class ProjectListView(ListView):
    model = Project
    ordering = ['-created_at']
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'


class ProjectCompleteview(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)

        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))

        if request.user != project.owner:
            return JsonResponse({"status": "error", "message": "Forbidden"}, status=403)

        if project.status != 'open':
            return JsonResponse({"status": "error", "message": "Project already closed"}, status=400)

        project.status = 'closed'
        project.save()
        return JsonResponse({"status": "ok", "project_status": "closed"})


class ProjectParticipate(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)

        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))

        if request.user in project.participants.all():
            project.participants.remove(request.user)
            participant = False
        else:
            project.participants.add(request.user)
            participant = True
        return JsonResponse({"status": "ok", "participant": participant})


class ProjectCreateView(CreateView):
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
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectModelForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})
