from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from .models import Cliente, Veiculo, Servico, Mecanico
from .forms import ClienteForm, VeiculoForm, ServicoForm

# 1. PÁGINA INICIAL
def home(request):
    return render(request, "oficina/home.html")

# 2. TELA DE BUSCA
def buscar(request):
    return render(request, "oficina/busca.html")

# 3. RESULTADO DA BUSCA (Corrigido para PostgreSQL com related_name)
def resultados(request):
    query = request.GET.get("q", "").strip()
    
    # IMPORTANTE: Mudamos 'servico_set' para 'servicos' porque 
    # você definiu related_name='servicos' no seu model Servico.
    veiculos = Veiculo.objects.filter(
        Q(placa__icontains=query) | Q(cliente__nome__icontains=query)
    ).select_related('cliente').prefetch_related('servicos').distinct()
    
    return render(request, "oficina/resultados.html", {
        "veiculos": veiculos, 
        "query": query
    })

# 4. OPERAÇÕES DE SERVIÇO (Criação e Edição)
def criar_servico(request):
    if request.method == "POST":
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redireciona para buscar para ver o resultado do novo serviço
            return redirect('buscar')
    else:
        form = ServicoForm()
    return render(request, "oficina/servico_form.html", {"form": form})

def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == "POST":
        form = ServicoForm(request.POST, request.FILES, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('buscar') 
    else:
        form = ServicoForm(instance=servico)
    return render(request, "oficina/servico_form.html", {"form": form, "editando": True})

# 5. GESTÃO DE MECÂNICOS (Painel de Estatísticas)
def painel_agentes(request):
    # Ajustado 'servico' para 'servicos' (o related_name que criamos)
    agentes = Mecanico.objects.annotate(total_servicos=Count('servicos'))
    return render(request, "oficina/painel_agentes.html", {"agentes": agentes})

def recrutar_agente(request):
    if request.method == "POST":
        nome_agente = request.POST.get("nome")
        especialidade = request.POST.get("especialidade")
        if nome_agente:
            Mecanico.objects.create(nome=nome_agente, especialidade=especialidade)
            return redirect('painel_agentes')
    return render(request, "oficina/cadastrar_mecanico.html")

# 6. CADASTRO UNIFICADO (Cliente + Veículo)
def mostrar_cadastro_unificado(request):
    return render(request, "oficina/cadastro_cliente_veiculo.html", {
        "cliente_form": ClienteForm(),
        "veiculo_form": VeiculoForm()
    })

def criar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
    # Se o nome da sua URL de cadastro for 'mostrar_cadastro_unificado', use esse nome:
    return redirect('cadastrar_tudo') 

def criar_veiculo(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('cadastrar_tudo')