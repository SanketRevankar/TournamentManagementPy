from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  # url(r'^ajax/open_/$', views.handler.htmlHelper.open_, name='open_'),
                  path('', views.welcome, name='welcome'),
                  path('api/v1/func/<str:name>', views.api_handler, name='api_handler'),
                  path('api/v1/func/get/<str:name>', views.get_api_handler, name='api_handler'),
                  path('api/v1/func/put/<str:name>', views.put_api_handler, name='api_handler'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
