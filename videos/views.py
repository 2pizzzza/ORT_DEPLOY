from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from my_tests.models import TestUser, Test
from users import permissions as p
from . import serializers as s, models as m
from .models import Video
from .serializers import VideoSerializer


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

        if user.is_authenticated:
            user_tests = TestUser.objects.filter(user=user, test__course=course_id)
            passed_test_ids = user_tests.values_list('test_id', flat=True)
            queryset = m.Video.objects.filter(course=course_id)
            queryset = queryset.exclude(test_id__in=passed_test_ids)
        else:
            queryset = m.Video.objects.filter(course=course_id)

        return queryset



class VideoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = m.Video.objects.all()
    serializer_class = s.VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VideoByTestIdAPIView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get(self, request, *args, **kwargs):
        test_id = kwargs.get('test_id')
        try:
            test = Test.objects.get(pk=test_id)
            video = test.video
            serializer = self.get_serializer(video)
            return Response(serializer.data)
        except Test.DoesNotExist:
            return Response({'error': 'Test not found'}, status=404)