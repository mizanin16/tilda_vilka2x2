from django.http import HttpResponseForbidden


class APIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        allowed_paths = ['/admin/', '/tilda-webhook/', '/promocode/', '/check-address/', '/add_user/']
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or any(
                path.startswith(allowed) for allowed in allowed_paths):
            return self.get_response(request)
        else:
            return HttpResponseForbidden("Доступ запрещен")
