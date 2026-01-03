from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Cliente, Veiculo, Servico
from .forms import ClienteForm, VeiculoForm, ServicoForm

# 1. Página Inicial
def home(request):
    return render(request, "oficina/home.html")

# 2. Tela de Busca
def buscar(request):
    return render(request, "oficina/busca.html")

# 3. Resultado da Busca (Com fotos, histórico e mecânico)
def resultados(request):
    query = request.GET.get("q", "").strip()
    # Busca na placa do carro OU no nome do cliente
    veiculos = Veiculo.objects.filter(
        Q(placa__icontains=query) | Q(cliente__nome__icontains=query)
    ).select_related('cliente').prefetch_related('servico_set').distinct()
    
    return render(request, "oficina/resultados.html", {
        "veiculos": veiculos, 
        "query": query
    })

# 4. Tela de Cadastro Unificado
def mostrar_cadastro_unificado(request):
    return render(request, "oficina/cadastro_cliente_veiculo.html", {
        "cliente_form": ClienteForm(),
        "veiculo_form": VeiculoForm()
    })

# 5. Lógica de Criação (Exemplos simplificados)
def criar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_tudo')
    return redirect('cadastrar_tudo')

def criar_veiculo(request):
    if request.method == "POST":
        # IMPORTANTE: request.FILES é necessário para as FOTOS
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_tudo')
    return redirect('cadastrar_tudo')

def criar_servico(request):
    if request.method == "POST":
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "oficina/servico_form.html", {"form": ServicoForm()})