from .models import Post
from django.utils.timezone import now
from celery import shared_task
import time
from celery import shared_task  # Used to mark a function as a Celery task
from celery.utils.log import get_task_logger  # U
logger = get_task_logger(__name__)


@shared_task(name="app.tasks.my_task")
def my_task():
    logger.info("Celery Task is being executed")

    time.sleep(10)
    print("Background  Work !!!!")


@shared_task
def publish_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.post_time <= now():
            post.is_published = True
            post.save()
            return f"Post '{post.title}' published successfully."
    except Post.DoesNotExist:
        return f"Post with ID {post_id} does not exist."
