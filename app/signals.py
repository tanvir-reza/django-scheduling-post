from django.db.models.signals import post_save
from django.dispatch import receiver
from celery import current_app
from .models import Post
from .tasks import publish_post


@receiver(post_save, sender=Post)
def schedule_post(sender, instance, created, **kwargs):
    if created:
        # Cancel previously scheduled task (if any)
        if hasattr(instance, '__celery_task_id') and instance.__celery_task_id:
            current_app.control.revoke(instance.__celery_task_id)

        # Schedule a new task
        eta = instance.post_time
        task = publish_post.apply_async((instance.id,), eta=eta)
        instance.__celery_task_id = task.id
        instance.save()
