from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    view_counts = models.PositiveIntegerField(default=0)
    url_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to='portfolio/images/')
    alt_txt = models.TextField(blank=True)
    caption = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def __str__(self):
        return f"{self.project.title} — image {self.sort_order}"


class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7)  # hex e.g. "#3B82F6"

    class Meta:
        verbose_name = "Project Technology"
        verbose_name_plural = "Project Technologies"

    def __str__(self):
        return f"{self.project.title} — {self.name}"
