from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Document(models.Model):
    """Основная модель документа"""
    
    title = models.CharField("Название документа", max_length=255)
    file = models.FileField("Файл", upload_to='documents/%Y/%m/%d/')
    content_hash = models.CharField("Хэш файла (SHA-256)", max_length=64, blank=True)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True)
    
    description = models.TextField("Описание", blank=True)
    version = models.CharField("Версия", max_length=20, default="1.0")
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.version})"