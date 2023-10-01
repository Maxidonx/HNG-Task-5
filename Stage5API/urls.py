from django.urls import path
from . import views

urlpatterns = [
    path('api/start-stream/', views.start_stream, name='start-stream'),
    path('api/stop-stream/', views.stop_stream, name='stop-stream'),
]
