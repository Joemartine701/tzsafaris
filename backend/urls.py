from django.urls import path

from .views.components.tour_views import tour
from .views.auth_views import login, register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('api/user', register, name='user'),
    path('api/sign-in', login, name='sign-in'),
    path('api/tour', tour, name='tour'),
    path('api/tour/<int:tour_id>/', tour, name='tour'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)