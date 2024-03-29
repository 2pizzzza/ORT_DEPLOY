from rest_framework import generics, permissions
from users import permissions as p
from . import serializers as s, models as m


class VideoCreateAPIView(generics.CreateAPIView):
    serializer_class = s.VideoSerializer
    permission_classes = [p.IsTeacher]


class VideoListAPIView(generics.ListAPIView):
    serializer_class = s.VideoSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        queryset = m.Video.objects.filter(course=course_id)
        return queryset


class VideoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = m.Video.objects.all()
    serializer_class = s.VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
