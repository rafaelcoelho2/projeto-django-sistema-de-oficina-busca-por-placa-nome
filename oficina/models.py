from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF", null=True, blank=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone/WhatsApp")
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome

class Mecanico(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.especialidade if self.especialidade else 'Geral'})"

class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="veiculos")
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10, unique=True) # Unique impede placas duplicadas
    ano = models.PositiveIntegerField(null=True, blank=True)
    foto_carro = models.ImageField(upload_to='veiculos/', blank=True, null=True) 
    obs_gerais = models.TextField(blank=True, null=True, verbose_name="Observações do Veículo")

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

class Servico(models.Model):
    STATUS_CHOICES = [
        ('orcamento', 'Orçamento'),
        ('aprovado', 'Aprovado / Em Manutenção'),
        ('finalizado', 'Finalizado'),
        ('entregue', 'Entregue ao Cliente'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name="servicos")
    mecanico = models.ForeignKey(Mecanico, on_delete=models.SET_NULL, null=True, verbose_name="Mecânico Responsável")
    
    descricao = models.TextField(verbose_name="O que foi feito no serviço")
    observacao_servico = models.TextField(blank=True, null=True, verbose_name="Observação para o Cliente")
    
    valor_pecas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_mao_de_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='orcamento')
    foto_local_servico = models.ImageField(upload_to='servicos/', blank=True, null=True) 
    data = models.DateTimeField(auto_now_add=True)

    @property
    def valor_total(self):
        return self.valor_pecas + self.valor_mao_de_obra

    def __str__(self): 
        return f"Serviço #{self.id} - {self.veiculo.placa} ({self.get_status_display()})"