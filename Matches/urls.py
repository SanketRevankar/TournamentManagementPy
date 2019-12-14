from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  # url(r'^ajax/open_/$', views.handler.htmlHelper.open_, name='open_'),
                  path('', views.welcome, name='welcome'),
                  path('Rules', views.rules, name='welcome'),
                  path('api/v1/get/get_match_data', views.get_matches, name='get_matches'),
                  path('api/v1/get/banner', views.get_banner, name='get_matches'),
                  path('api/v1/get/<str:match_id>', views.get_match_data, name='get_match_data'),
                  path('<str:match_id>', views.match_details, name='match_details'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
