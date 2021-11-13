from django.db import models

from hashlib import md5


class Urls(models.Model):
    full_url = models.URLField(unique=True)
    hash_url = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.hash_url = md5(self.full_url.encode()).hexdigest()[:10]

        return super().save(*args, **kwargs)
