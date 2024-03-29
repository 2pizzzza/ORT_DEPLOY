from rest_framework import generics, permissions

from . import models as m, serializers as s
from users import permissions as p

class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = s.CourseSerializer
    permission_classes = [p.IsTeacher]


class CourseListAPIView(generics.ListAPIView):
    queryset = m.Course.objects.all()
    serializer_class = s.CourseSerializer


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = m.Course.objects.all()
    serializer_class = s.CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
