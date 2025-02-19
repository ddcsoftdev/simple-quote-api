from django.db import models
import uuid


class Quote(models.Model):
    """Base Quote model class"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(null = False, blank=False, max_length=200, verbose_name="Author")
    content = models.TextField(null=False, blank=False, verbose_name="Text Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    
    def __str__(self):
        return f"{self.author}: {self.content}"
    
    class Meta:
        ordering = ["-created_at"]
