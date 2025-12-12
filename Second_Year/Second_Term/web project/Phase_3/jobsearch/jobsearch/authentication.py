from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication that doesn't enforce CSRF for API endpoints.
    This is useful for development and when using token-based authentication.
    """
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
