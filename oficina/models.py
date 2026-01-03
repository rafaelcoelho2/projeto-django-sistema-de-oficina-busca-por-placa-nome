from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    def __str__(self): return self.nome

class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10)
    foto_carro = models.ImageField(upload_to='veiculos/', blank=True, null=True) 
    
    # ESTE CAMPO resolve o erro do FieldError
    obs_gerais = models.TextField(blank=True, null=True, verbose_name="Observações do Veículo")

    def __str__(self): return f"{self.modelo} ({self.placa})"

class Servico(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    descricao = models.TextField()
    foto_local_servico = models.ImageField(upload_to='servicos/', blank=True, null=True) 
    data = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Serviço em {self.veiculo} - {self.data.strftime('%d/%m/%Y')}"