from django.views.generic import ListView, DetailView
from django.views import View
from projects.models import Project

from django.shortcuts import get_object_or_404
from django.http import JsonResponse


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
