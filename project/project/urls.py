from django.contrib import admin
from django.urls import path, include
from news.views import user_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/', user_profile, name='user_profile'),
]
