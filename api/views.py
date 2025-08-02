from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Assignment, Submission, User
from .serializers import AssignmentSerializer, SubmissionSerializer, UserSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsTeacher , IsStudent




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Assignment.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Submission.objects.filter(assignment__teacher=self.request.user)
    


class StudentSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)




class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]
    queryset = Assignment.objects.all()
