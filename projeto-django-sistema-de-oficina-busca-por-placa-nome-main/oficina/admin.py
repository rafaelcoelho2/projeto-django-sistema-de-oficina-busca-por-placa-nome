from django.contrib import admin
from .models import Cliente, Veiculo, Servico

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone')

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'cliente')
    search_fields = ('placa', 'modelo', 'cliente__nome')

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'data', 'descricao')
    list_filter = ('data',)
