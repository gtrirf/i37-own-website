from rest_framework import serializers
from .models import BlogType, Blog, BlogImage


class BlogTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogType
        fields = ['id', 'type_name']


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'photo', 'alt_txt', 'caption', 'sort_order']


class BlogListSerializer(serializers.ModelSerializer):
    blog_type = BlogTypeSerializer(read_only=True)
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'view_counts', 'blog_type', 'first_image', 'created_at']

    def get_first_image(self, obj):
        image = obj.images.first()
        if image:
            return BlogImageSerializer(image, context=self.context).data
        return None


class BlogDetailSerializer(serializers.ModelSerializer):
    blog_type = BlogTypeSerializer(read_only=True)
    images = BlogImageSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'view_counts', 'blog_type', 'images', 'created_at', 'updated_at']
