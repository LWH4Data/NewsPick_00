from django.db import models
from pgvector.django import VectorField

# Create your models here.
class NewsArticle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    summary = models.TextField()
    updated = models.DateTimeField()
    full_text = models.TextField(default='')
    category = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    embedding = VectorField(dimensions=1536, blank=True, null=True)

    def __str__(self):
        return self.title