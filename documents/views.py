from django.shortcuts import render
from .models import Document


def document_list(request):
    """Список всех документов"""
    documents = Document.objects.all().order_by('-uploaded_at')
    
    context = {
        'documents': documents,
        'title': 'Документы'
    }
    return render(request, 'documents/document_list.html', context)