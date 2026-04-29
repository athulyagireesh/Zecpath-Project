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
from core.views import CandidateProfileAPI, EmployerProfileAPI

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/signup/', SignupAPI.as_view()),
    path('api/login/', LoginAPI.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('api/jobs/', JobListAPI.as_view()),
    # path('api/jobs/create/', JobCreateAPI.as_view()),
    path('api/jobs/create/', JobCreateAPI.as_view()),
    path('api/apply/', ApplyJobAPI.as_view()),
    path('api/users/', UserTestAPI.as_view()),
    path('api/candidate/profile/', CandidateProfileAPI.as_view()),
    path('api/employer/profile/', EmployerProfileAPI.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
