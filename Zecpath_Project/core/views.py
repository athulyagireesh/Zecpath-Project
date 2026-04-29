from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Job, CustomUser, Application
from .serializers import JobSerializer, UserSerializer , CandidateSerializer, EmployerSerializer
from .permissions import IsAdmin, IsEmployer, IsCandidate
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


# ✅ Signup
class SignupAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        if CustomUser.objects.filter(email=request.data.get("email")).exists():
            return Response({"error": "Email already exists"}, status=400)
        return super().create(request, *args, **kwargs)


# ✅ Login
class LoginAPI(TokenObtainPairView):
    pass


# ✅ Employer → Create Job
class JobCreateAPI(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def post(self, request):
        try:
            employer = request.user.employer
        except:
            return Response({"error": "Employer profile not found"}, status=400)

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(employer=employer)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)





class JobListAPI(generics.ListAPIView):
    queryset = Job.objects.select_related('employer', 'employer__user').all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'description']




# ✅ Candidate → Apply Job
class ApplyJobAPI(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, request):
        job_id = request.data.get('job')

        try:
            candidate = request.user.candidate
        except:
            return Response({"error": "Candidate profile not found"}, status=400)

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=404)

        if Application.objects.filter(job=job, candidate=candidate).exists():
            return Response({"error": "Already applied"}, status=400)

        Application.objects.create(job=job, candidate=candidate)

        return Response({"message": "Applied successfully"}, status=201)


# ✅ Admin → View Users
class UserTestAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    



class CandidateProfileAPI(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]
    parser_classes = [MultiPartParser, FormParser]   # 👈 ADD THIS LINE

    def get(self, request):
        candidate = request.user.candidate
        return Response(CandidateSerializer(candidate).data)

    def put(self, request):
        candidate = request.user.candidate
        serializer = CandidateSerializer(candidate, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request):
        candidate = request.user.candidate
        candidate.is_active = False
        candidate.save()
        return Response({"message": "Profile soft deleted"})
    



class EmployerProfileAPI(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request):
        employer = request.user.employer
        return Response(EmployerSerializer(employer).data)

    def put(self, request):
        employer = request.user.employer
        serializer = EmployerSerializer(employer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request):
        employer = request.user.employer
        employer.is_active = False
        employer.save()
        return Response({"message": "Profile soft deleted"})
    

    