import redis
from django.http import JsonResponse
from core.settings import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        key = f"rate_limit:{ip}"
        count = redis_client.incr(key)

        if count == 1:
            redis_client.expire(key, 10)  # 60 seconds

        if count > 5:
            return JsonResponse({"error": "Too many requests"}, status=429)

        return self.get_response(request)
