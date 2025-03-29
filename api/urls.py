from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ai/', views.aiView, name='ai'),
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path("posts/", views.all_posts, name="all_posts"),
    path("create-post/", views.create_post, name="create_post"),
    path("my-posts/", views.my_posts, name="my_posts"),
    path("all-posts/", views.all_posts, name="all_posts"),
    path("delete-post/<int:pk>/", views.delete_post, name="delete_post"),
    path("update-post/<int:pk>/", views.update_post, name="update_post"),
    path("post-details/<int:pk>/", views.post_details, name="post_detail"),
    path("logout/", views.logout_view, name="logout"),

]