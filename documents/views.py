from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View

import os
import mimetypes

from .models import Document


def document_list(request):
    """Список всех документов"""
    documents = Document.objects.all().order_by('-uploaded_at')
    
    context = {
        'documents': documents,
        'title': 'Документы'
    }
    return render(request, 'documents/document_list.html', context)


@login_required
def download_document(request, pk):
    """Скачивание документа с оригинальным именем"""
    document = get_object_or_404(Document, pk=pk)

    if document.uploaded_by != request.user and not request.user.is_staff:
        raise Http404("Нет доступа к файлу")

    if not document.file or not os.path.exists(document.file.path):
        raise Http404("Файл не найден")

    download_name = document.original_filename or os.path.basename(document.file.name)

    content_type, _ = mimetypes.guess_type(download_name)
    if content_type is None:
        content_type = 'application/octet-stream'

    response = FileResponse(
        open(document.file.path, 'rb'),
        as_attachment=True,
        filename=download_name,
        content_type=content_type
    )
    return response


class DocumentDeleteView(LoginRequiredMixin, View):
    """Простое удаление документа без промежуточной страницы"""
    
    def get(self, request, pk):
        """GET — сразу удаляем (с проверкой)"""
        document = get_object_or_404(Document, pk=pk)
        
        # Проверка прав
        if document.uploaded_by != request.user and not request.user.is_staff:
            messages.error(request, "У вас нет прав на удаление этого документа.")
            return redirect('documents:document_list')
        
        # Безопасное удаление (файл + запись в БД)
        title = document.title
        document.delete()  # вызовет переопределённый delete() в модели
        
        messages.success(request, f'Документ "{title}" успешно удалён.')
        return redirect('documents:document_list')