from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from comments.models import Comment

# Create your models here.

#Post.objects.all()
#Post.objects.create(user=user, title=title)


class PostManager(models.Manager):
    #  this can override built in model managers similar to those listed above
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()  # this is an example of overwriting objects.all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now()).order_by('-publish')


def upload_location(instance, filename):
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "{}/{}".format(new_id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True,
                              width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.title  # this is what i see in the django admin page, instead of 'post object'

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def get_markdown(self):
        content = self.content
        print("Content: ", content)
        print()
        markdown_text = markdown(content)
        print("Markdown Text: ", markdown_text)
        print()
        print("Mark Safe: ", mark_safe(markdown_text))
        my_test_1 = """
        <p><a href="http://www.google.com">google</a>
        second try
        <img src="http://animalsbreeds.com/wp-content/uploads/2014/06/Schipperke-10.jpg" alt="cody"></p>
        """
        my_test_2 = """
        <p><a href="http%3A%2F%2Fwww.google.com">google</a>
        second try
        <img src="http%3A%2F%2Fanimalsbreeds.com%2Fwp-content%2Fuploads%2F2014%2F06%2FSchipperke-10.jpg" alt="cody" /></p>
        """

        """
        This doesnt work using the mark-deux method. I get this error back on the django console
        [04/Dec/2016 10:41:00] "GET /posts/cody-2/ HTTP/1.1" 200 3637
        Not Found: /posts/cody-2/http://animalsbreeds.com/wp-content/uploads/2014/06/Schipperke-10.jpg
        [04/Dec/2016 10:41:00] "GET /posts/cody-2/http%3A%2F%2Fanimalsbreeds.com%2Fwp-content%2Fuploads%2F2014%2F06%2FSchipperke-10.jpg HTTP/1.1" 404 3327
        """
        return mark_safe(my_test_1)  # this works and represents the jquery method
        #return mark_safe(my_test_2)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

# This is a recursive function
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "{}-{}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


# Anytime something is saved, its going to go through this pre-save function first.
pre_save.connect(pre_save_post_receiver, sender=Post)
