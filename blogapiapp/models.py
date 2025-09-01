from django.db import models

class post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

