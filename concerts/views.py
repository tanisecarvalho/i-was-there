from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Concert, Band
from .forms import CommentForm, ConcertForm, BandForm


class ConcertList(generic.ListView):
    model = Concert
    queryset = Concert.objects.order_by('-created_on')
    template_name = 'concerts.html'
    paginate_by = 6
    context_object_name = "concerts"

    def get_queryset(self, **kwargs):
        band = self.request.GET.get('band')
        country = self.request.GET.get('country')

        if band and country:
            concerts = concerts = self.model.objects.filter(
                    band__in=Band.objects.filter(name__icontains=band),
                    country__icontains=country
                )
        elif band or country:
            if band:
                concerts = self.model.objects.filter(
                    band__in=Band.objects.filter(name__icontains=band)
                )
            if country:
                concerts = self.model.objects.filter(
                    country__icontains=country
                )
        else:
            concerts = self.model.objects.all()
        return concerts


class ConcertDetail(LoginRequiredMixin, View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Concert.objects
        concert = get_object_or_404(queryset, pk=slug)
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


class AddToMyList(LoginRequiredMixin, View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Concert.objects
        concert = get_object_or_404(queryset, pk=slug)

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
        concert = get_object_or_404(queryset, pk=slug)

        comment_form = CommentForm(data=request.POST, files=request.FILES)

        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment = comment_form.save(commit=False)
            comment.concert = concert
            comment.save()
            concert.goers.add(request.user)
        else:
            comment_form = CommentForm()

        return redirect("concert_detail", slug=concert.pk)


class AddConcert(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        return render(
            request,
            "add_concert.html",
            {
                "band_form": BandForm(),
                "concert_form": ConcertForm(),
                "comment_form": CommentForm()
            },
        )

    def post(self, request, *args, **kwargs):

        band_form = BandForm(data=request.POST)
        concert_form = ConcertForm(data=request.POST)
        comment_form = CommentForm(data=request.POST, files=request.FILES)

        query_band = Band.objects.filter(name=request.POST['name'])

        if query_band.exists():
            band = get_object_or_404(query_band)
        else:
            if band_form.is_valid():
                band_form.instance.user = request.user
                band = band_form.save()

        if concert_form.is_valid():
            concert_form.instance.user = request.user
            concert = concert_form.save(commit=False)
            concert.band = band
            print(band)
            concert.save()

            if comment_form.is_valid():
                comment_form.instance.user = request.user
                comment = comment_form.save(commit=False)
                comment.concert = concert
                comment.save()
                concert.goers.add(request.user)

                return redirect("concert_detail", slug=concert.pk)
        else:
            band_form = BandForm()
            concert_form = ConcertForm()
            comment_form = CommentForm()

            return render(
                request,
                "add_concert.html",
                {
                    "band_form": BandForm(),
                    "concert_form": ConcertForm(),
                    "comment_form": CommentForm()
                },
            )


class MyConcertList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        concerts = Concert.objects.filter(goers=self.request.user.id)
        return render(
            request,
            "concerts.html",
            {
                "concerts": concerts
            },
        )


class EditConcert(LoginRequiredMixin, View):

    def get(self, request, slug, *args, **kwargs):

        queryset = Concert.objects
        concert = get_object_or_404(queryset, pk=slug)

        if concert.user == request.user:
            band_form = BandForm(instance=concert.band)
            concert_form = ConcertForm(instance=concert)

            return render(
                request,
                "edit_concert.html",
                {
                    "band_form": band_form,
                    "concert_form": concert_form
                },
            )

    def post(self, request, slug, *args, **kwargs):

        queryset = Concert.objects
        concert = get_object_or_404(queryset, pk=slug)

        band_form = BandForm(data=request.POST)
        concert_form = ConcertForm(data=request.POST, instance=concert)

        query_band = Band.objects.filter(name=request.POST['name'])

        if query_band.exists():
            band = get_object_or_404(query_band)
        else:
            if band_form.is_valid():
                band_form.instance.user = request.user
                band = band_form.save()

        if concert_form.is_valid():
            concert_form.instance.band = band
            concert_form.save()

            return redirect("concert_detail", slug=concert.pk)
        else:
            band_form = BandForm(instance=concert.band)
            concert_form = ConcertForm(instance=concert)

            return render(
                request,
                "edit_concert.html",
                {
                    "band_form": band_form,
                    "concert_form": concert_form,
                },
            )


class DeleteConcert(LoginRequiredMixin, View):
    def get(self, request, slug, *args, **kwargs):

        queryset = Concert.objects
        concert = get_object_or_404(queryset, pk=slug)

        if concert.user == request.user:

            return render(
                request,
                "delete_concert.html"
            )
        else:
            return redirect('403')

    def post(self, request, slug, *args, **kwargs):

        queryset = Concert.objects
        concert = get_object_or_404(queryset, pk=slug)

        concert.delete()
        return redirect('home')
