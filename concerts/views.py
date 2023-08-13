from django.shortcuts import render
from django.views import generic
from .models import Concert


class ConcertList(generic.ListView):
    model = Concert
    queryset = Concert.objects.order_by('-created_on')
    template_name = 'concerts.html'
    paginate_by = 6
