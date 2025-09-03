from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Assignment, Submission, User
from .serializers import (AssignmentSerializer,SubmissionSerializer,UserSerializer,RegisterSerializer)
from .permissions import IsTeacher, IsStudent
from django.http import FileResponse, Http404
from .tasks import generate_pdf_task
import os
from rest_framework.views import APIView



class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Return the authenticated user's profile (no ID required)."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="register", permission_classes=[])
    def register(self, request):
        """Public endpoint for user registration."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data)

    
    



class AssignmentViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Assignment.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class SubmissionViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Submission.objects.filter(assignment__teacher=self.request.user)


class StudentSubmissionViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               GenericViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Assignment.objects.all()
    
    
    
class PDFGenerateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        output_path = os.path.join("C:\\temp", f"generated_pdf_user_{user.id}.pdf")  # Match the task path

        if not os.path.exists(output_path):
            generate_pdf_task.delay(user.id)
            return Response({"detail": "The PDF is generating please wait 1 minute"}, status=202)

        try:
            return FileResponse(open(output_path, 'rb'), content_type='application/pdf', filename='report.pdf')
        except FileNotFoundError:
            raise Http404("PDF file not found.")