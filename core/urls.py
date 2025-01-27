from django.urls import path, include

urlpatterns = [
    path('visualisation/', include('core.visualisation.visualisation_urls')),
]
