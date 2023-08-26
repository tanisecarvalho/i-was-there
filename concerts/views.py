from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from .models import Concert
from .forms import CommentForm


class ConcertList(generic.ListView):
    model = Concert
    queryset = Concert.objects.order_by('-created_on')
    template_name = 'concerts.html'
    paginate_by = 6


class ConcertDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Concert.objects
        concert = get_object_or_404(queryset, slug=slug)
        comments = concert.comments.order_by('-created_on')
        photos = []
        for comment in comments:
            if 'placeholder' not in comment.photo.url:
                photos.append(comment)

        return render(
            request,
            "view_concert.html",
            {
                "concert": concert,
                "comments": comments,
                "photos": photos
            },
        )


class AddToMyList(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Concert.objects
        concert = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            "add_to_my_list.html",
            {
                "concert": concert,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Concert.objects
        concert = get_object_or_404(queryset, slug=slug)

        comment_form = CommentForm(data=request.POST, files=request.FILES)

        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment = comment_form.save(commit=False)
            comment.concert = concert
            comment.save()
        else:
            comment_form = CommentForm()

        return redirect("concert_detail", slug=concert.slug)
