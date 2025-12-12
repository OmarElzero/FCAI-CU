from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from .models import Application
from .serializers import ApplicationSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_company:
            return queryset.filter(job__company=user.company)
        return queryset.filter(user=user)
