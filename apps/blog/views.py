from django.db.models import F
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import BlogType, Blog
from .serializers import BlogTypeSerializer, BlogListSerializer, BlogDetailSerializer


class BlogTypeListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogTypeSerializer
    queryset = BlogType.objects.all()


class BlogListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogListSerializer

    def get_queryset(self):
        queryset = Blog.objects.select_related('blog_type').prefetch_related('images')
        blog_type = self.request.query_params.get('type')
        search = self.request.query_params.get('search')
        if blog_type:
            queryset = queryset.filter(blog_type_id=blog_type)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset


class BlogDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogDetailSerializer
    queryset = Blog.objects.select_related('blog_type').prefetch_related('images')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_counts = F('view_counts') + 1
        instance.save(update_fields=['view_counts'])
        instance.refresh_from_db(fields=['view_counts'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
