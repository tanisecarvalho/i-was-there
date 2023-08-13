from . import views
from django.urls import path


urlpatterns = [
    path('', views.ConcertList.as_view(), name='home')
]
