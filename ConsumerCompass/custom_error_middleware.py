# custom_error_middleware.py

from django.shortcuts import redirect
from django.conf import settings

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            # Log the exception if needed
            if settings.DEBUG:
                return redirect('/')  # Replace with your error URL
            raise e
