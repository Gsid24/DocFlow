from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('documents.urls')),           # ← корневая страница = список
    path('documents/', include('documents.urls')), # ← на всякий случай
]

# Для разработки — чтобы MEDIA-файлы (загруженные документы) отдавались
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)