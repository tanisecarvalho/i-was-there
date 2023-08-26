from . import views
from django.urls import path


urlpatterns = [
    path('', views.ConcertList.as_view(), name='home'),
    path('add-concert/', views.AddConcert.as_view(), name='add_concert'),
    path('<slug:slug>/', views.ConcertDetail.as_view(), name='concert_detail'),
    path('<slug:slug>/add-to-my-list/', views.AddToMyList.as_view(), name='add_to_my_list'),
]
