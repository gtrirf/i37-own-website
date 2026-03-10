from rest_framework import serializers
from .models import Project, ProjectImage, ProjectTechnology


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'photo', 'alt_txt', 'caption', 'sort_order']


class ProjectTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTechnology
        fields = ['id', 'name', 'color']


class ProjectListSerializer(serializers.ModelSerializer):
    technologies = ProjectTechnologySerializer(many=True, read_only=True)
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'content', 'view_counts', 'url_link', 'technologies', 'first_image', 'created_at']

    def get_first_image(self, obj):
        image = obj.images.first()
        if image:
            return ProjectImageSerializer(image, context=self.context).data
        return None


class ProjectDetailSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    technologies = ProjectTechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'content', 'view_counts', 'url_link', 'images', 'technologies', 'created_at', 'updated_at']
