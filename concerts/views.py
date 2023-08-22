from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Concert


class ConcertList(generic.ListView):
    model = Concert
    queryset = Concert.objects.order_by('-created_on')
    template_name = 'concerts.html'
    paginate_by = 6


class ConcertDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Concert.objects
        concert = get_object_or_404(queryset, slug=slug)
        comments = concert.comments.order_by('created_on')

        return render(
            request,
            "view_concert.html",
            {
                "concert": concert,
                "comments": comments
            },
        )
