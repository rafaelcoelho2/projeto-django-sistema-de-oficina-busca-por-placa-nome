from django.urls import path
from . import views

urlpatterns = [
    # --- Navegação Principal ---
    path("", views.home, name="home"),
    
    # --- Sistema de Busca e Inteligência ---
    path("buscar/", views.buscar, name="buscar"),
    path("resultados/", views.resultados, name="resultados"),
    
    # --- Painel de Monitoramento e Gestão de Agentes ---
    path("agentes/", views.painel_agentes, name="painel_agentes"),
    path("agentes/recrutar/", views.recrutar_agente, name="recrutar_agente"),
    
    # --- Cadastros de Base (Cliente e Veículo) ---
    # AJUSTADO: Agora o nome coincide com o redirect das views
    path("cadastro/", views.mostrar_cadastro_unificado, name="mostrar_cadastro_unificado"),
    path("criar_cliente/", views.criar_cliente, name="criar_cliente"),
    path("criar_veiculo/", views.criar_veiculo, name="criar_veiculo"),
    
    # --- Operações de Serviço (Dossiês) ---
    path("servico/", views.criar_servico, name="criar_servico"),
    
    # Rota de Edição
    path("servico/editar/<int:pk>/", views.editar_servico, name="editar_servico"),
]