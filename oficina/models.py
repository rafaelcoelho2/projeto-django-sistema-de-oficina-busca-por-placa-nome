from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    def __str__(self): return self.nome

# Criamos uma tabela para os mecânicos
class Mecanico(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self): return self.nome

class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10)
    foto_carro = models.ImageField(upload_to='veiculos/', blank=True, null=True) 
    # Observação fixa do carro (ex: arranhões, detalhes permanentes)
    obs_gerais = models.TextField(blank=True, null=True, verbose_name="Observações do Veículo")

    def __str__(self): return f"{self.modelo} ({self.placa})"

class Servico(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    # Agora o mecânico é selecionado da lista de mecânicos cadastrados
    mecanico = models.ForeignKey(Mecanico, on_delete=models.SET_NULL, null=True, verbose_name="Mecânico Responsável")
    
    descricao = models.TextField(verbose_name="O que foi feito no serviço")
    
    # NOVO CAMPO: Observação específica deste serviço (ex: "Trocar óleo daqui a 5mil km")
    observacao_servico = models.TextField(blank=True, null=True, verbose_name="Observação para o Cliente")
    
    foto_local_servico = models.ImageField(upload_to='servicos/', blank=True, null=True) 
    data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return f"Serviço em {self.veiculo} - {self.data.strftime('%d/%m/%Y')}"