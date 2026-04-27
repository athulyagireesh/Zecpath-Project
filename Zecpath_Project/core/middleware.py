from django.http import JsonResponse


class RoleCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith('/api/login') or request.path.startswith('/api/signup'):
            return self.get_response(request)

        # user = request.user
        user = getattr(request, 'user', None)

        if user.is_authenticated:

            if request.path.startswith('/api/jobs/create/'):
                if user.role != 'employer':
                    return JsonResponse({"error": "Only employers can create jobs"}, status=403)

            if request.path.startswith('/api/apply/'):
                if user.role != 'candidate':
                    return JsonResponse({"error": "Only candidates can apply"}, status=403)

            if request.path.startswith('/api/users/'):
                if user.role != 'admin':
                    return JsonResponse({"error": "Only admin can access"}, status=403)

        return self.get_response(request)