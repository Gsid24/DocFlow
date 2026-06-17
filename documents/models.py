from django.db import models
from django.contrib.auth.models import User
import unicodedata
import os


def transliterate_filename(filename):
    """Безопасная транслитерация имени файла"""
    if not filename:
        return "document"
    
    # Разделяем имя и расширение
    name, ext = os.path.splitext(filename)
    
    # Транслитерируем только имя
    name = unicodedata.normalize('NFKD', str(name))
    name = name.encode('ASCII', 'ignore').decode('ASCII')
    name = name.strip().replace(' ', '_').replace('__', '_')
    
    # Если после транслита имя пустое — оставляем оригинальное
    if not name:
        name = "document"
    
    return name + ext


class Document(models.Model):
    """Основная модель документа"""
    
    title = models.CharField("Название документа", max_length=255)
    
    file = models.FileField(
        "Файл", 
        upload_to='documents/%Y/%m/%d/',
        max_length=500
    )
    
    original_filename = models.CharField("Оригинальное имя файла", max_length=255, blank=True)
    
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

    def save(self, *args, **kwargs):
        if self.file and not self.original_filename:
            self.original_filename = self.file.name
            # Транслитерируем имя файла
            if self.file.name:
                self.file.name = transliterate_filename(self.file.name)
        
        super().save(*args, **kwargs)