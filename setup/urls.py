from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # 1. Rotas de Autenticação (Coloque antes da oficina para garantir prioridade)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 2. Rotas da sua Aplicação
    path("", include("oficina.urls")),
]

# Configuração para arquivos de mídia (Fotos/Uploads)
# Isso funciona tanto em DEBUG quanto no Railway se o WhiteNoise estiver ok
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Garante que as mídias funcionem em produção se você não usar S3/Cloudinary
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)