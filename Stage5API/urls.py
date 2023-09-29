from django.urls import path
from .views import video_list, create_video, get_video

urlpatterns = [
    path('videos/', video_list, name='video_list'),
    path('videos/create/', create_video, name='create_video'),
    path('videos/<int:pk>/', get_video, name='get_video'),
]