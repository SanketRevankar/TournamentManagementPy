from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from Servers.api import query_server
from . import views

urlpatterns = [
                  path('', views.welcome, name='welcome'),
                  path('AdminRequests', views.requests, name='requests'),
                  path('Admins/<str:server_id>', views.admins, name='admins'),
                  path('api/v1/get/server_data', query_server.get_server_data, name='get_server_data'),
                  path('api/v1/post/adminship_request', query_server.adminship_request, name='adminship_request'),
                  path('api/v1/post/adminship_response', query_server.adminship_response, name='adminship_response'),
                  path('api/v1/post/update_admin', query_server.update_admin, name='update_admin'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
