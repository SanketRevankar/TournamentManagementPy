from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('create', views.create_team, name='create_team'),
                  path('manage', views.manage_team, name='manage_team'),
                  path('edit', views.edit_team, name='edit_team'),
                  path('delete', views.delete_team, name='edit_team'),
                  path('join/<str:team_id>', views.join_team, name='api_handler'),
                  path('api/v1/func/<str:name>', views.api_handler, name='api_handler'),
                  path('leave', views.leave_team, name='api_handler'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
