from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Job
from .serializers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        company = self.request.query_params.get('company')
        status = self.request.query_params.get('status')
        if company:
            queryset = queryset.filter(company=company)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
