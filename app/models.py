from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_time = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        # cheking if the post created or updated
        is_created = self._state.adding
        super().save(*args, **kwargs)
        if is_created:
            from .tasks import publish_post
            publish_post.apply_async((self.id,), eta=self.post_time)
        
