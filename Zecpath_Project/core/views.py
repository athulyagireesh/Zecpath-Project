from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Job, CustomUser, Application
from .serializers import JobSerializer, UserSerializer , CandidateSerializer, EmployerSerializer
from .permissions import IsAdmin, IsEmployer, IsCandidate
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import ApplicationSerializer
from .permissions import IsCandidate
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter




class JobPagination(PageNumberPagination):
    page_size = 5



class SignupAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")

        # ✅ check email exists in request
        if not email:
            return Response({"error": "Email is required"}, status=400)

        # ✅ check duplicate properly
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        return super().create(request, *args, **kwargs)



# ✅ Login
class LoginAPI(TokenObtainPairView):
    pass






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








class JobUpdateAPI(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def put(self, request, pk):
        employer = request.user.employer

        try:
            job = Job.objects.get(id=pk, employer=employer)
        except Job.DoesNotExist:
            return Response({"error": "Not allowed"}, status=403)

        serializer = JobSerializer(job, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)









class JobToggleAPI(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def post(self, request, pk):
        employer = request.user.employer

        try:
            job = Job.objects.get(id=pk, employer=employer)
        except Job.DoesNotExist:
            return Response({"error": "Not allowed"}, status=403)

        job.status = 'inactive' if job.status == 'active' else 'active'
        job.save()

        return Response({"status": job.status})








class JobListAPI(generics.ListAPIView):
    queryset = Job.objects.filter(status='active').select_related('employer','employer__user')
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    pagination_class = JobPagination

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = {
        'skills': ['exact'],
        'location': ['exact'],
        'job_type': ['exact'],
        'experience': ['gte', 'lte'],
        'salary_min': ['gte'],
        'salary_max': ['lte'],
    }

    search_fields = ['title', 'description', 'skills']




class ApplyJobAPI(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, request):
        job_id = request.data.get('job')

        try:
            candidate = request.user.candidate
        except:
            return Response({"error": "Candidate profile not found"}, status=400)

        try:
            job = Job.objects.get(id=job_id, status='active')
        except Job.DoesNotExist:
            return Response({"error": "Job not available"}, status=404)

        # ❌ Duplicate prevention
        if Application.objects.filter(job=job, candidate=candidate).exists():
            return Response({"error": "Already applied"}, status=400)

        # ✅ Resume binding
        resume = candidate.resume

        application = Application.objects.create(
            job=job,
            candidate=candidate,
            resume=resume
        )

        return Response({
            "message": "Applied successfully",
            "application_id": application.id
        }, status=201)





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
    

    


class MyApplicationsAPI(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return Application.objects.filter(
            candidate=self.request.user.candidate
        ).select_related('job')
    



class UpdateApplicationStatusAPI(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def post(self, request, pk):
        employer = request.user.employer

        try:
            application = Application.objects.select_related('job').get(id=pk)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=404)

        # ✅ Ownership check
        if application.job.employer != employer:
            return Response({"error": "Not allowed"}, status=403)

        new_status = request.data.get("status")

        valid_transitions = {
            'applied': ['shortlisted', 'rejected'],
            'shortlisted': ['interview', 'rejected'],
            'interview': ['selected', 'rejected'],
            'selected': [],
            'rejected': []
        }

        current_status = application.status

        if new_status not in valid_transitions.get(current_status, []):
            return Response({
                "error": f"Cannot move from {current_status} → {new_status}"
            }, status=400)

        application.status = new_status
        application.save()

        return Response({
            "message": "Status updated",
            "new_status": application.status
        })
    




class EmployerJobsAPI(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return Job.objects.filter(
            employer=self.request.user.employer
        )
    










class JobApplicantsAPI(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    filter_backends = [SearchFilter]
    search_fields = ['candidate__user__email']

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return Application.objects.filter(
            job__id=job_id,
            job__employer=self.request.user.employer
        )
    






class EmployerAnalyticsAPI(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request):
        employer = request.user.employer

        total_jobs = Job.objects.filter(employer=employer).count()
        total_applications = Application.objects.filter(job__employer=employer).count()
        shortlisted = Application.objects.filter(
            job__employer=employer,
            status='shortlisted'
        ).count()

        return Response({
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "shortlisted": shortlisted
        })
    









class AppliedJobsAPI(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return Application.objects.filter(
            candidate=self.request.user.candidate
        ).select_related('job')
    
    
    




class RecommendedJobsAPI(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):
        candidate = self.request.user.candidate
        skills = candidate.skills

        return Job.objects.filter(
            skills__icontains=skills,
            status='active'
        )