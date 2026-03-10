from django.db.models import F
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectListSerializer, ProjectDetailSerializer


class ProjectListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProjectListSerializer
    queryset = Project.objects.prefetch_related('images', 'technologies')


class ProjectDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.prefetch_related('images', 'technologies')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_counts = F('view_counts') + 1
        instance.save(update_fields=['view_counts'])
        instance.refresh_from_db(fields=['view_counts'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
