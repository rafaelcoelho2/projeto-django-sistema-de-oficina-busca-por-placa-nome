from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required # Protege as telas
from .models import Cliente, Veiculo, Servico, Mecanico
from .forms import ClienteForm, VeiculoForm, ServicoForm

# 1. PÁGINA INICIAL
def home(request):
    return render(request, "oficina/home.html")

# 2. TELA DE BUSCA (Protegida)
@login_required
def buscar(request):
    return render(request, "oficina/busca.html")

# 3. RESULTADO DA BUSCA (Filtra pelo Usuário Logado)
@login_required
def resultados(request):
    query = request.GET.get("q", "").strip()
    
    # FILTRO DE PRIVACIDADE: cliente__usuario=request.user
    # Isso garante que você só veja veículos de clientes que VOCÊ cadastrou.
    veiculos = Veiculo.objects.filter(
        Q(placa__icontains=query) | Q(cliente__nome__icontains=query),
        cliente__usuario=request.user 
    ).select_related('cliente').distinct()
    
    return render(request, "oficina/resultados.html", {
        "veiculos": veiculos, 
        "query": query
    })

# 4. OPERAÇÕES DE SERVIÇO
@login_required
def criar_servico(request):
    if request.method == "POST":
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            # Aqui não precisamos travar o usuário, pois o Veículo já tem dono
            form.save()
            return redirect('buscar')
    else:
        # Filtra os veículos no formulário para mostrar apenas os do usuário
        form = ServicoForm()
        form.fields['veiculo'].queryset = Veiculo.objects.filter(cliente__usuario=request.user)
        
    return render(request, "oficina/servico_form.html", {"form": form})

@login_required
def editar_servico(request, pk):
    # O get_object_or_404 aqui deve garantir que o serviço pertence ao usuário
    servico = get_object_or_404(Servico, pk=pk, veiculo__cliente__usuario=request.user)
    if request.method == "POST":
        form = ServicoForm(request.POST, request.FILES, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('buscar') 
    else:
        form = ServicoForm(instance=servico)
    return render(request, "oficina/servico_form.html", {"form": form, "editando": True})

# 5. GESTÃO DE MECÂNICOS
@login_required
def painel_agentes(request):
    # Mostra apenas mecânicos do usuário (se você adicionou o campo usuario no modelo Mecanico)
    agentes = Mecanico.objects.filter(usuario=request.user).annotate(total_servicos=Count('servicos'))
    return render(request, "oficina/painel_agentes.html", {"agentes": agentes})

@login_required
def recrutar_agente(request):
    if request.method == "POST":
        nome_agente = request.POST.get("nome")
        especialidade = request.POST.get("especialidade")
        if nome_agente:
            Mecanico.objects.create(
                nome=nome_agente, 
                especialidade=especialidade,
                usuario=request.user # Salva quem recrutou
            )
            return redirect('painel_agentes')
    return render(request, "oficina/cadastrar_mecanico.html")

# 6. CADASTRO UNIFICADO
@login_required
def mostrar_cadastro_unificado(request):
    return render(request, "oficina/cadastro_cliente_veiculo.html", {
        "cliente_form": ClienteForm(),
        "veiculo_form": VeiculoForm()
    })

@login_required
def criar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user # ATRIBUI O DONO
            cliente.save()
    return redirect('mostrar_cadastro_unificado') 

@login_required
def criar_veiculo(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            # Como o Veículo é ligado ao Cliente, e o Cliente já tem dono, 
            # você só precisa garantir que o mecânico não cadastre carro para cliente de outro.
            form.save()
    return redirect('mostrar_cadastro_unificado')