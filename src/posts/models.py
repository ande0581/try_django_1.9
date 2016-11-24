from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


def upload_location(instance, filename):
    """ This puts the file in the instance pk folder"""
    return "{}/{}".format(instance.id, filename)


class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True,
                              width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title  # this is what i see in the django admin page, instead of 'post object'

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.id})
