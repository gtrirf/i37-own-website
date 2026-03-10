from django.db import models
from django.core.exceptions import ValidationError


class MainInfo(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='main/')
    text = models.TextField()

    class Meta:
        verbose_name = "Main Info"
        verbose_name_plural = "Main Info"

    def __str__(self):
        return self.name

    def clean(self):
        if MainInfo.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Only one MainInfo record is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Career(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='career/logos/')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Career"
        verbose_name_plural = "Careers"

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    class Platform(models.TextChoices):
        TELEGRAM = 'telegram', 'Telegram'
        INSTAGRAM = 'instagram', 'Instagram'
        LINKEDIN = 'linkedin', 'LinkedIn'
        X = 'x', 'X (Twitter)'
        YOUTUBE = 'youtube', 'YouTube'
        GITHUB = 'github', 'GitHub'

    app = models.CharField(max_length=50, choices=Platform.choices)
    url = models.URLField()

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.app
