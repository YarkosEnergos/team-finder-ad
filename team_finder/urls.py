from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def root_redirect(request):
    return redirect('/project/list/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect),
    path('project/', include('projects.urls')),
    path('projects/', include('projects.urls')),
    path('users/', include('users.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
