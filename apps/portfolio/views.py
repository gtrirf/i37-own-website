from django.db.models import F
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.pagination import StandardPagination
from .models import Project
from .serializers import ProjectListSerializer, ProjectDetailSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='search', description='Loyiha nomi boyicha qidirish', required=False, type=str),
        OpenApiParameter(name='tech', description='Texnologiya nomi boyicha filter (masalan: Django)', required=False, type=str),
        OpenApiParameter(name='page', description='Sahifa raqami', required=False, type=int),
        OpenApiParameter(name='page_size', description='Sahifadagi elementlar soni (max: 100)', required=False, type=int),
    ]
)
class ProjectListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProjectListSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = Project.objects.prefetch_related('images', 'technologies')
        search = self.request.query_params.get('search')
        tech = self.request.query_params.get('tech')
        if search:
            queryset = queryset.filter(title__icontains=search)
        if tech:
            queryset = queryset.filter(technologies__name__icontains=tech).distinct()
        return queryset


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
