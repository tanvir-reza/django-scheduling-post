from django.shortcuts import render
# HTTPResponse is a class that takes a string as an argument and returns an HTTP response object.
from django.http import HttpResponse
import redis

# Create your views here.
def index(request):

    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    redis_client.set("name", "John Doe")

    name = redis_client.get("name")
    print(name)

    return HttpResponse("Hello, world. You're at the polls index.")