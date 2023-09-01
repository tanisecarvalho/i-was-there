from . import views
from django.urls import path


urlpatterns = [
    path('', views.ConcertList.as_view(), name='concerts'),
    path('my-concerts/', views.MyConcertList.as_view(), name='my_concerts'),
    path('add-concert/', views.AddConcert.as_view(), name='add_concert'),
    path('<slug:slug>/', views.ConcertDetail.as_view(), name='concert_detail'),
    path('add-to-my-list/<slug:slug>/', views.AddToMyList.as_view(), name='add_to_my_list'),
    path('edit-concert/<slug:slug>/', views.EditConcert.as_view(), name='edit_concert'),
    path('delete-concert/<slug:slug>/', views.DeleteConcert.as_view(), name='delete_concert'),
]
