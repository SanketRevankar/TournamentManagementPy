from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  # url(r'^ajax/open_/$', views.handler.htmlHelper.open_, name='open_'),
                  path('', views.welcome, name='welcome'),
                  path('Rules', views.rules, name='rules'),
                  path('Stats', views.stats, name='stats'),
                  path('Stats/TopStats', views.top_stats, name='top_stats'),
                  path('Stats/Team/<str:team>', views.team_stats, name='team_stats'),
                  path('api/v1/get/get_match_data', views.get_matches, name='get_matches'),
                  path('api/v1/get/<str:match_id>', views.get_match_data, name='get_match_data'),
                  path('Stats/api/v1/get/top/<str:stat>', views.get_top_stats, name='get_top_stats'),
                  path('<str:match_id>', views.match_details, name='match_details'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
