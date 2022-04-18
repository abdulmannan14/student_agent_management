from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# from limoucloud_backend.utils import unique_slug_generator

from django.utils.text import slugify
import random
import string


def random_str_generate(size=4) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(size))


def unique_slug_generator(instance, new_slug=None, extra=""):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify("{} {}".format(instance.title, extra))

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_str_generate(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


class Feature(models.Model):
    title = models.CharField(max_length=200, null=True, blank=False)
    is_included = models.BooleanField(null=False, blank=False, default=True)

    def __str__(self):
        return self.title


class Package(models.Model):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    pricing_durations = [
        (MONTHLY, MONTHLY),
        (YEARLY, YEARLY)
    ]
    title = models.CharField(max_length=200, null=True, blank=False)
    price = models.FloatField(default=0.0, null=True, blank=False, help_text="")
    allowed_trips = models.IntegerField(default=0, null=True, blank=False)
    pricing_duration = models.CharField(max_length=50, null=True, blank=False, choices=pricing_durations)
    features = models.ManyToManyField(Feature, related_name="package_features")
    short_description = models.TextField(max_length=200, null=True, blank=False,help_text="You can add html as well")
    is_active = models.BooleanField(default=True, null=False, blank=False)
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            return self.get_details()
        except:
            return self.title

    def get_details(self):
        return "{}-{}{}/{} ({} team members)".format(self.title, "$", self.price, self.pricing_duration,
                                                     self.allowed_trips)

    def get_duration(self):
        if self.pricing_duration == self.MONTHLY:
            return "month"
        return "year"

    @property
    def yearly_price(self):
        return self.price * 12


@receiver(pre_save, sender=Package)
def pkg_slug_generate(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, extra=instance.pricing_duration)
