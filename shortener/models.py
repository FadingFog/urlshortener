from django.db import models
from django.conf import settings

from hashlib import md5
from random import sample


class Url(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    full_url = models.URLField()
    hash_url = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                hash_url = md5(self.full_url.encode()).hexdigest()
                self.hash_url = ''.join(sample(hash_url, len(hash_url)))[:10]  # shuffle md5 url
                try:
                    _ = Url.objects.get(hash_url=hash_url)
                except:
                    return super().save(*args, **kwargs)

        return super().save(*args, **kwargs)
