from django.db import models
from django.contrib.auth.models import User
import os
import uuid
from datetime import datetime


def get_safe_filename(original_filename: str) -> str:
    """Генерирует безопасное имя для хранения на диске"""
    if not original_filename:
        return f"document_{uuid.uuid4().hex[:8]}.bin"

    basename = os.path.basename(str(original_filename))
    name, ext = os.path.splitext(basename)

    # Простая транслитерация
    name = name.encode('ASCII', 'ignore').decode('ASCII').strip()
    name = ''.join(c for c in name if c.isalnum() or c in ('-', '_', '.'))
    name = name.replace(' ', '_').replace('__', '_')

    if not name:
        name = "document"

    unique_name = f"{name}_{uuid.uuid4().hex[:8]}"
    return unique_name + ext.lower()


def document_upload_to(instance, filename: str) -> str:
    """Callable для upload_to"""
    safe_name = get_safe_filename(filename)
    now = datetime.now()
    return f'documents/{now.year}/{now.month:02d}/{now.day:02d}/{safe_name}'


class Document(models.Model):
    title = models.CharField("Название документа", max_length=255)
    
    file = models.FileField(
        "Файл",
        upload_to=document_upload_to,
        max_length=500
    )
    
    original_filename = models.CharField(
        "Оригинальное имя файла", 
        max_length=255, 
        blank=True,
        editable=False
    )
    
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
        # Сохраняем оригинальное имя при первой загрузке
        if self.file and not self.original_filename:
            self.original_filename = os.path.basename(self.file.name)
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Переопределяем удаление — удаляем и файл с диска"""
        if self.file:
            try:
                if self.file.storage.exists(self.file.name):
                    self.file.delete(save=False)  # удаляем файл
            except Exception as e:
                print(f"Ошибка при удалении файла {self.file.name}: {e}")
        
        super().delete(*args, **kwargs)