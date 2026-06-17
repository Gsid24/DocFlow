from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

import os
import mimetypes

from .models import Document   # ← Важно! Добавь эту строку


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


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление документа"""
    model = Document
    template_name = 'documents/document_confirm_delete.html'
    success_url = reverse_lazy('documents:document_list')
    
    def get_queryset(self):
        """Только свои документы или staff"""
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(uploaded_by=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f'Документ "{self.object.title}" успешно удалён.')
        return super().form_valid(form)