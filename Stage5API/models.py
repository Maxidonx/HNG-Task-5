from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from functools import partial

# Define the make_stream_key function
make_stream_key = partial(get_random_string, 20)

class Stream(models.Model):
    key = models.CharField(max_length=20, default=make_stream_key, unique=True)
    started_at = models.DateTimeField(null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    transcription = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Stream {self.id}'

    @property
    def is_live(self):
        return self.started_at is not None

    @property
    def hls_url(self):
        return reverse("hls-url", args=(self.key,))
