from django.contrib import admin
from .models import Cliente, Mecanico, Veiculo, Servico

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Exibe o CPF e Telefone na listagem
    list_display = ('nome', 'cpf', 'telefone')
    search_fields = ('nome', 'cpf')

@admin.register(Mecanico)
class MecanicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especialidade', 'ativo')
    list_filter = ('especialidade', 'ativo')
    search_fields = ('nome',)

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    # Mostra a placa e o dono (cliente) logo de cara
    list_display = ('placa', 'modelo', 'cliente', 'ano')
    search_fields = ('placa', 'modelo', 'cliente__nome')
    list_filter = ('modelo', 'ano')

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    # list_display controla as colunas que aparecem na tabela principal
    list_display = ('id', 'veiculo', 'mecanico', 'status', 'data', 'valor_total')
    
    # Adiciona filtros na lateral direita para facilitar a gestão
    list_filter = ('status', 'data', 'mecanico')
    
    # Permite pesquisar pelo nome do cliente ou pela placa do carro
    search_fields = ('veiculo__placa', 'veiculo__cliente__nome', 'descricao')
    
    # Organiza os campos dentro da tela de edição do serviço
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('veiculo', 'mecanico', 'status')
        }),
        ('Detalhes do Serviço', {
            'fields': ('descricao', 'observacao_servico', 'foto_local_servico')
        }),
        ('Financeiro', {
            'fields': ('valor_pecas', 'valor_mao_de_obra')
        }),
    )

    # Função para exibir o valor total (soma de peças + mão de obra) na lista
    def valor_total(self, obj):
        return f"R$ {obj.valor_total}"
    valor_total.short_description = 'Total do Serviço'