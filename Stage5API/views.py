from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Stream
from .serializers import StreamSerializer
from django.views.decorators.csrf import csrf_exempt
import logging

# For video transcription


logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def start_stream(request):
    try:
        stream_key = request.data.get("name")
        stream = get_object_or_404(Stream, key=stream_key)

        if stream.started_at:
            return Response(f"Stream {stream_key} is already streaming", status=403)

        stream.started_at = timezone.now()
        stream.save()

        serializer = StreamSerializer(stream)
        return Response(serializer.data)

    except Stream.DoesNotExist:
        return Response(f"Stream {stream_key} not found", status=404)
    except Exception as e:
        logger.error(f"Error starting stream {stream_key}: {str(e)}")
        return Response(f"An error occurred while starting stream {stream_key}", status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def stop_stream(request):
    try:
        stream_key = request.data.get("name")
        stream = get_object_or_404(Stream, key=stream_key)

        stream.started_at = None
        stream.save()

        serializer = StreamSerializer(stream)
        return Response(serializer.data)

    except Stream.DoesNotExist:
        return Response(f"Stream {stream_key} not found", status=404)
    except Exception as e:
        logger.error(f"Error stopping stream {stream_key}: {str(e)}")
        return Response(f"An error occurred while stopping stream {stream_key}", status=500)

# This is a placeholder function. You'll need to implement the actual video streaming and transcription functionality.
def transcribe_video(stream_key):
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = f"./{stream_key}.wav"

    with open(file_name, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))