from django.http import JsonResponse

class BlockPUTRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'PUT':
            return JsonResponse(
                {'error': 'PUT requests are not allowed.'},
                status=405
            )
        return self.get_response(request)
