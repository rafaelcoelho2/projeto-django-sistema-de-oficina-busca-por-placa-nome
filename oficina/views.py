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

# 3. RESULTADO DA BUSCA
def resultados(request):
    query = request.GET.get("q", "").strip()
    
    # IMPORTANTE: Se o histórico não aparece, vamos usar o padrão do Django: 'servico_set'
    # ou garantir que o nome coincida com o seu Model.
    veiculos = Veiculo.objects.filter(
        Q(placa__icontains=query) | Q(cliente__nome__icontains=query)
    ).select_related('cliente').prefetch_related('servico_set').distinct()
    
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
            return redirect('buscar')
    else:
        form = ServicoForm()
    return render(request, "oficina/servico_form.html", {"form": form})

# ... (outras funções de editar_servico permanecem iguais)

# 5. GESTÃO DE MECÂNICOS
def painel_agentes(request):
    # Corrigido: Usando 'servico' (singular) conforme o erro que o Django te deu antes
    agentes = Mecanico.objects.annotate(total_servicos=Count('servico'))
    return render(request, "oficina/painel_agentes.html", {"agentes": agentes})

# ... (funções de cadastro unificado permanecem iguais)