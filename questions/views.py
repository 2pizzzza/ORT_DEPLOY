from rest_framework import generics, permissions

from . import models as m, serializers as s
from users import permissions as p


class QuestionCreateAPIView(generics.CreateAPIView):
    serializer_class = s.QuestionSerializer
    permission_classes = [p.IsTeacher]


class QuestionListAPIView(generics.ListAPIView):
    serializer_class = s.QuestionSerializer

    def get_queryset(self):
        test_id = self.kwargs.get('pk')
        queryset = m.Question.objects.filter(test=test_id)
        return queryset


class QuestionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = m.Question.objects.all()
    serializer_class = s.QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AnswerCreateAPIView(generics.CreateAPIView):
    serializer_class = s.AnswerSerializer
    permission_classes = [p.IsTeacher]
    def perform_create(self, serializer):
        serializer.save()
        return serializer.instance


class AnswerListAPIView(generics.ListAPIView):
    serializer_class = s.AnswerSerializer

    def get_queryset(self):
        question_id = self.kwargs.get('pk')
        queryset = m.Answer.objects.filter(question=question_id)
        return queryset


class AnswerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = m.Answer.objects.all()
    serializer_class = s.AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
