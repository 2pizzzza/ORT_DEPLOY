from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users import permissions as p
from . import serializers as s, models as m
from .models import Video


class VideoCreateAPIView(generics.CreateAPIView):
    serializer_class = s.VideoSerializer
    permission_classes = [p.IsTeacher]


class AddUserToWatchedVideo(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        video.user_watched.add(user)
        return Response("User added to watched list for this video.")


class VideoListAPIView(generics.ListAPIView):
    serializer_class = s.VideoSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        user = self.request.user
        queryset = m.Video.objects.filter(course=course_id)

        if user.is_authenticated:
            queryset = queryset.exclude(test__testuser__user=user)
        return queryset


class VideoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = m.Video.objects.all()
    serializer_class = s.VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
