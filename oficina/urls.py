from django.urls import path
from . import views

urlpatterns = [
    # --- Navegação Principal ---
    path("", views.home, name="home"),
    
    # --- Autenticação e Acesso ---
    # Garanta que o nome seja 'cadastrar' para bater com os botões dos templates
    path("cadastrar/", views.cadastrar_usuario, name="cadastrar"),
    
    # --- Sistema de Busca ---
    path("buscar/", views.buscar, name="buscar"),
    path("resultados/", views.resultados, name="resultados"),
    
    # --- Gestão de Agentes (Mecânicos) ---
    path("agentes/", views.painel_agentes, name="painel_agentes"),
    path("agentes/recrutar/", views.recrutar_agente, name="recrutar_agente"),
    
    # --- Cadastros de Base ---
    path("cadastro/", views.mostrar_cadastro_unificado, name="mostrar_cadastro_unificado"),
    path("criar_cliente/", views.criar_cliente, name="criar_cliente"),
    path("criar_veiculo/", views.criar_veiculo, name="criar_veiculo"),
    
    # --- Operações de Serviço ---
    path("servico/", views.criar_servico, name="criar_servico"),
    path("servico/editar/<int:pk>/", views.editar_servico, name="editar_servico"),
]