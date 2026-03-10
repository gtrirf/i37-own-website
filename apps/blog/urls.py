from django.urls import path
from .views import BlogTypeListView, BlogListView, BlogDetailView

urlpatterns = [
    path('blog-types/', BlogTypeListView.as_view(), name='blog-type-list'),
    path('blog/', BlogListView.as_view(), name='blog-list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
]
