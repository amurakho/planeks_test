from django.db import models
from django.contrib.auth.models import AbstractUser
from uuslug import slugify

from authorization.models import CustomUser


class Pub(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, unique=True)
    is_pub = models.BooleanField(default=False, verbose_name='Was published')
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        permissions = (
            ('can_publish', 'Can published'),
        )

    def get_comments(self):
        return Comment.objects.filter(pub=self)


class Comment(models.Model):
    pub = models.ForeignKey(Pub, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
