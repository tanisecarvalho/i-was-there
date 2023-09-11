from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Concert, Band, Comment
from .forms import CommentForm, ConcertForm, BandForm
from django.core.exceptions import PermissionDenied


class ConcertList(LoginRequiredMixin, generic.ListView):
    """ View to list all the new concerts """
    model = Concert
    queryset = Concert.objects.order_by('-created_on')
    template_name = 'concerts.html'
    paginate_by = 6
    context_object_name = "concerts"

    def get_queryset(self, **kwargs):
        band = self.request.GET.get('band')
        country = self.request.GET.get('country')

        if band and country:
            concerts = self.model.objects.filter(
                band__in=Band.objects.filter(name__icontains=band),
                country__icontains=country
            ).exclude(goers=self.request.user.id)
        elif band or country:
            if band:
                concerts = self.model.objects.filter(
                    band__in=Band.objects.filter(name__icontains=band)
                ).exclude(goers=self.request.user.id)
            if country:
                concerts = self.model.objects.filter(
                    country__icontains=country
                ).exclude(goers=self.request.user.id)
        else:
            concerts = self.model.objects.all().exclude(
                goers=self.request.user.id
                )
        return concerts


class ConcertDetail(LoginRequiredMixin, View):
    """ View to show details about a concert """

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
    """ View to add a concert to the user list """

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
            messages.add_message(
                request,
                messages.SUCCESS,
                'Concert added to your list.')
        else:
            comment_form = CommentForm()

        return redirect("concert_detail", slug=concert.pk)


class AddConcert(LoginRequiredMixin, View):
    """ View to create a new concert """

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
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Concert created and added to your list.')

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


class MyConcertList(LoginRequiredMixin, generic.ListView):
    """ View to show the list of concerts the user has added to themselves """
    model = Concert
    queryset = Concert.objects.order_by('-created_on')
    template_name = 'my_concerts.html'
    paginate_by = 6
    context_object_name = "concerts"

    def get_queryset(self, **kwargs):
        band = self.request.GET.get('band')
        country = self.request.GET.get('country')

        if band and country:
            concerts = self.model.objects.filter(
                band__in=Band.objects.filter(name__icontains=band),
                country__icontains=country,
                goers=self.request.user.id
            )
        elif band or country:
            if band:
                concerts = self.model.objects.filter(
                    band__in=Band.objects.filter(name__icontains=band),
                    goers=self.request.user.id
                )
            if country:
                concerts = self.model.objects.filter(
                    country__icontains=country,
                    goers=self.request.user.id
                )
        else:
            concerts = self.model.objects.filter(goers=self.request.user.id)
        return concerts


class EditConcert(LoginRequiredMixin, View):
    """ View to edit the details about a concert """

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
        else:
            raise PermissionDenied

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

            messages.add_message(
                request,
                messages.SUCCESS,
                'Concert was edited successfully.')

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
    """ View to delete a concert """
    def get(self, request, slug, *args, **kwargs):

        try:
            Concert.objects.get(pk=slug, goers=request.user)
        except Concert.DoesNotExist:
            raise PermissionDenied

        return render(
            request,
            "delete_concert.html"
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Concert.objects
        concert = get_object_or_404(queryset, pk=slug)

        if concert.user != request.user:
            comments = Comment.objects.filter(
                concert=concert,
                user=request.user
                )
            comments.delete()
            concert.goers.remove(request.user)
            messages.add_message(
                request,
                messages.SUCCESS,
                'Concert was removed from your list.')
            return redirect('my_concerts')
        else:
            if (concert.number_of_goers() > 1):
                queryUser = User.objects
                admin = get_object_or_404(queryUser, pk=1)
                comments = Comment.objects.filter(
                    concert=concert,
                    user=request.user
                    )
                comments.delete()
                concert.goers.remove(request.user)
                concert.user = admin
                concert.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Concert transfered to admin and removed from your list.')
                return redirect('my_concerts')
            else:
                concert.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Concert was deleted successfully.')
                return redirect('my_concerts')
