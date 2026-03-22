from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Cliente, Veiculo, Servico, Mecanico
from .forms import ClienteForm, VeiculoForm, ServicoForm, UsuarioRegistroForm

# 1. PÁGINA INICIAL
def home(request):
    return render(request, "oficina/home.html")

# 2. TELA DE BUSCA (Protegida)
@login_required
def buscar(request):
    return render(request, "oficina/busca.html")

# 3. RESULTADO DA BUSCA
@login_required
def resultados(request):
    query = request.GET.get("q", "").strip()
    veiculos = Veiculo.objects.filter(
        Q(placa__icontains=query) | Q(cliente__nome__icontains=query),
        cliente__usuario=request.user 
    ).select_related('cliente').distinct()
    
    return render(request, "oficina/resultados.html", {
        "veiculos": veiculos, 
        "query": query
    })

# 4. CADASTRO DE USUÁRIO
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('buscar')
    else:
        form = UsuarioRegistroForm()
    return render(request, 'registration/cadastrar.html', {'form': form})

# 5. OPERAÇÕES DE SERVIÇO
@login_required
def criar_servico(request):
    if request.method == "POST":
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('buscar')
    else:
        form = ServicoForm()
        form.fields['veiculo'].queryset = Veiculo.objects.filter(cliente__usuario=request.user)
        form.fields['mecanico'].queryset = Mecanico.objects.filter(usuario=request.user)
        
    return render(request, "oficina/servico_form.html", {"form": form})

@login_required
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk, veiculo__cliente__usuario=request.user)
    if request.method == "POST":
        form = ServicoForm(request.POST, request.FILES, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('buscar') 
    else:
        form = ServicoForm(instance=servico)
        form.fields['veiculo'].queryset = Veiculo.objects.filter(cliente__usuario=request.user)
        form.fields['mecanico'].queryset = Mecanico.objects.filter(usuario=request.user)
    return render(request, "oficina/servico_form.html", {"form": form, "editando": True})

# 6. GESTÃO DE MECÂNICOS (AQUI ESTAVA O ERRO)
@login_required
def painel_agentes(request):
    # CORREÇÃO: Mudado de 'servicos' para 'servico' (nome do modelo em minúsculo)
    agentes = Mecanico.objects.filter(usuario=request.user).annotate(total_servicos=Count('servico'))
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
                usuario=request.user
            )
            return redirect('painel_agentes')
    return render(request, "oficina/cadastrar_mecanico.html")

# 7. CADASTRO UNIFICADO
@login_required
def mostrar_cadastro_unificado(request):
    cliente_form = ClienteForm()
    veiculo_form = VeiculoForm()
    veiculo_form.fields['cliente'].queryset = Cliente.objects.filter(usuario=request.user)
    
    return render(request, "oficina/cadastro_cliente_veiculo.html", {
        "cliente_form": cliente_form,
        "veiculo_form": veiculo_form
    })

@login_required
def criar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
    return redirect('mostrar_cadastro_unificado') 

@login_required
def criar_veiculo(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            veiculo = form.save(commit=False)
            if veiculo.cliente.usuario == request.user:
                veiculo.save()
    return redirect('mostrar_cadastro_unificado')