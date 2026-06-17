from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('<int:pk>/download/', views.download_document, name='download_document'),
    path('<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document_delete'),
]