from django.urls import path
from . import views

urlpatterns = [
    # Página Inicial (base.html / home)
    path("", views.home, name="home"),
    
    # Busca de Veículos (busca.html e resultados.html)
    path("buscar/", views.buscar, name="buscar"),
    path("resultados/", views.resultados, name="resultados"),
    
    # Cadastros (cadastro_cliente_veiculo.html e formulario_unico.html)
    path("cadastro/", views.mostrar_cadastro_unificado, name="cadastrar_tudo"),
    path("criar_cliente/", views.criar_cliente, name="criar_cliente"),
    path("criar_veiculo/", views.criar_veiculo, name="criar_veiculo"),
    
    # Serviços (servico_form.html)
    path("servico/", views.criar_servico, name="criar_servico"),
]