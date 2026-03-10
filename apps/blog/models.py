from django.db import models


class BlogType(models.Model):
    type_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Blog Type"
        verbose_name_plural = "Blog Types"

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    view_counts = models.PositiveIntegerField(default=0)
    blog_type = models.ForeignKey(
        BlogType, on_delete=models.SET_NULL, null=True, blank=True, related_name='blogs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to='blog/images/')
    alt_txt = models.TextField(blank=True)
    caption = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Blog Image"
        verbose_name_plural = "Blog Images"

    def __str__(self):
        return f"{self.blog.title} — image {self.sort_order}"
