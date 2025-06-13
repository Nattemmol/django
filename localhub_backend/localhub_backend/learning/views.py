from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Course, Progress, Certificate, Quiz, Assignment, AssignmentSubmission
from .serializers import CourseSerializer, ProgressSerializer, CertificateSerializer, QuizSerializer, AssignmentSerializer, AssignmentSubmissionSerializer

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

class CourseProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        data = request.data.copy()
        data['user'] = request.user.id
        data['course'] = pk
        serializer = ProgressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CertificateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            cert = Certificate.objects.get(user=request.user, course_id=pk)
            serializer = CertificateSerializer(cert)
            return Response(serializer.data)
        except Certificate.DoesNotExist:
            return Response({"error": "Certificate not found"}, status=404)

class CertificateDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        cert = get_object_or_404(Certificate, user=request.user, course_id=pk)
        # Assuming cert_url is a path to the file on the server
        try:
            return FileResponse(open(cert.cert_url, 'rb'), as_attachment=True, filename='certificate.pdf')
        except FileNotFoundError:
            raise Http404("Certificate file not found.")

class QuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['pk']
        return Quiz.objects.filter(course_id=course_id)

class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        course_id = self.kwargs['pk']
        return Assignment.objects.filter(course_id=course_id)

class AssignmentSubmissionView(generics.CreateAPIView):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        assignment_id = self.kwargs['pk']
        serializer.save(user=self.request.user, assignment_id=assignment_id)
