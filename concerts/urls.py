from . import views
from django.urls import path


urlpatterns = [
    path('', views.ConcertList.as_view(), name='home'),
    path('<slug:slug>/', views.ConcertDetail.as_view(), name='concert_detail'),
    path('add-to-my-list/<slug:slug>', views.AddToMyList.as_view(), name='add_to_my_list'),
]
