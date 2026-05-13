"""
URL configuration for Zecpath_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path 
from core.views import SignupAPI, LoginAPI, JobCreateAPI, JobListAPI, ApplyJobAPI, UserTestAPI 
from rest_framework_simplejwt.views import TokenRefreshView
from core.views import MyApplicationsAPI
from core.views import CandidateProfileAPI, EmployerProfileAPI, JobUpdateAPI,JobToggleAPI
from core.views import UpdateApplicationStatusAPI , EmployerJobsAPI ,JobApplicantsAPI , EmployerAnalyticsAPI , AppliedJobsAPI , RecommendedJobsAPI , ApproveEmployerAPI , BlockUserAPI ,  RemoveJobAPI , PlatformStatsAPI ,  AdminLogsAPI 
from core.views import ResumeParserAPI
from core.views import ResumeNLPAPI
from core.views import ATSMatchAPI
from core.views import AutoShortlistAPI
from core.views import ManualStatusOverrideAPI
from core.views import EligibilityCheckAPI
from core.views import NotificationLogsAPI


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/signup/', SignupAPI.as_view()),
    path('api/login/', LoginAPI.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('api/jobs/', JobListAPI.as_view()),
    path('api/jobs/create/', JobCreateAPI.as_view()),
    path('api/jobs/update/<int:pk>/', JobUpdateAPI.as_view()),
    path('api/jobs/toggle/<int:pk>/', JobToggleAPI.as_view()),
    path('api/apply/', ApplyJobAPI.as_view()),
    path('api/my-applications/', MyApplicationsAPI.as_view()),
    path('api/users/', UserTestAPI.as_view()),
    path('api/candidate/profile/', CandidateProfileAPI.as_view()),
    path('api/employer/profile/', EmployerProfileAPI.as_view()),
    path('api/application/status/<int:pk>/', UpdateApplicationStatusAPI.as_view()),
    path('api/employer/jobs/', EmployerJobsAPI.as_view()),
    path('api/job/<int:job_id>/applicants/', JobApplicantsAPI.as_view()),
    path('api/employer/analytics/', EmployerAnalyticsAPI.as_view()),
    path('api/candidate/applied-jobs/', AppliedJobsAPI.as_view()),
    path('api/candidate/recommended-jobs/', RecommendedJobsAPI.as_view()),
    path('api/admin/approve-employer/<int:pk>/', ApproveEmployerAPI.as_view()),
    path('api/admin/block-user/<int:pk>/', BlockUserAPI.as_view()),
    path('api/admin/remove-job/<int:pk>/', RemoveJobAPI.as_view()),
    path('api/admin/platform-stats/', PlatformStatsAPI.as_view()),
    path('api/admin/logs/', AdminLogsAPI.as_view()),
    path('api/resume-parser/', ResumeParserAPI.as_view()),
    path('api/resume-nlp/', ResumeNLPAPI.as_view()),
    path('api/ats-match/<int:job_id>/',ATSMatchAPI.as_view()),
    path('api/auto-shortlist/<int:job_id>/',AutoShortlistAPI.as_view()),
    path('api/manual-status/<int:application_id>/',ManualStatusOverrideAPI.as_view()),
    path('api/eligibility/<int:application_id>/',EligibilityCheckAPI.as_view()),
    path('api/notification-logs/',NotificationLogsAPI.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
