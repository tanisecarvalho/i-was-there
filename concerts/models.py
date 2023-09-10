from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Band(models.Model):
    """ Model to save the Bands info """
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bands"
        )
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Concert(models.Model):
    """ Model to save the Concert info """
    band = models.ForeignKey(
        Band,
        on_delete=models.CASCADE,
        related_name="concerts_bands"
        )
    date = models.DateField()
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="concerts"
        )
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    goers = models.ManyToManyField(
        User,
        related_name="concert_goers",
        blank=True
        )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.band} - {self.date}"

    def number_of_goers(self):
        return self.goers.count()


class Comment(models.Model):
    """ Model to save the Comment info """
    sentence = models.TextField()
    photo = CloudinaryField('image', default='placeholder')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
        )
    concert = models.ForeignKey(
        Concert,
        on_delete=models.CASCADE,
        related_name="comments"
        )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment {self.sentence} by {self.user}"
