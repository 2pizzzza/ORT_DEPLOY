from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import models as m, serializers as s
from users import permissions as p
from .models import TestUser


class TestCreateAPIView(generics.CreateAPIView):
    serializer_class = s.TestSerializer
    permission_classes = [p.IsTeacher]

    def perform_create(self, serializer):
        serializer.save()
        return serializer.instance


class TestListAPIView(generics.ListAPIView):
    serializer_class = s.TestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        queryset = m.Test.objects.filter(course=course_id)

        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = queryset.exclude(testuser__user=user)
        return queryset

    def get(self, request, *args, **kwargs):
        course_id = self.kwargs.get('pk')
        tests = m.Test.objects.filter(course=course_id)
        user = request.user

        unfinished_tests = [
            test for test in tests
            if not m.TestUser.objects.filter(test=test, user=user).exists()
        ]

        serializer = self.get_serializer(unfinished_tests, many=True)
        return Response(serializer.data)


class TestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = m.Test.objects.all()
    serializer_class = s.TestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TestUserCreateAPIView(generics.CreateAPIView):
    queryset = m.TestUser.objects.all()
    serializer_class = s.TestUserSerializerForSubmit
    permission_classes = [p.IsStudent, IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id

        user = request.user

        test = get_object_or_404(m.Test, pk=data['test'])

        if user in test.video.user_watched.all() and test == test.video.test:
            r_answers = data['right_answers']
            questions = test.questions.count()

            if self.queryset.filter(user=user, test=test).exists():
                return Response(
                    {'message': 'Вы уже проходили этот тест'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if r_answers > questions:
                return Response(
                    {'message': 'Количество вопросов меньше '
                        'общего количества переданных ответов'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {'message': 'Вы сдали тест', **serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Вы не можете пройти этот тест. '
                            'Вам нужно сначала посмотреть видео и соответствующий тест.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TestUserListAPIView(generics.ListAPIView):
    queryset = TestUser.objects.all()
    serializer_class = s.TestUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestUserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = s.TestUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestUserByUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        test_users = m.TestUser.objects.filter(user=user)
        serializer = s.TestUserSerializer(test_users, many=True)
        return Response(serializer.data)