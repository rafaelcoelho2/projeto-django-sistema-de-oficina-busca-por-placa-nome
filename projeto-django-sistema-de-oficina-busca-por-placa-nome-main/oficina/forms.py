from django import forms
from .models import Cliente, Veiculo, Servico, Mecanico

# 1. FORMULÁRIO DE CLIENTE
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone']

# 2. FORMULÁRIO DE VEÍCULO
class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['cliente', 'modelo', 'placa', 'foto_carro', 'obs_gerais']
        widgets = {
            'obs_gerais': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Ex: Manutenção preventiva pendente...'
            }),
        }

# 3. FORMULÁRIO DE SERVIÇO (ADAPTADO)
class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        # IMPORTANTE: Adicionei 'mecanico' aqui para ele aparecer no seu HTML
        fields = ['veiculo', 'mecanico', 'descricao', 'observacao_servico', 'foto_local_servico']
        
        widgets = {
            'veiculo': forms.Select(attrs={'style': 'background: #000; color: #0f0; border: 1px solid #333;'}),
            'mecanico': forms.Select(attrs={'style': 'background: #000; color: #0f0; border: 1px solid #333;'}),
            'descricao': forms.Textarea(attrs={
                'rows': 3, 
                'style': 'background: #000; color: #0f0; border: 1px solid #333;',
                'placeholder': 'RELATÓRIO TÉCNICO...'
            }),
            'observacao_servico': forms.Textarea(attrs={
                'rows': 2, 
                'style': 'background: #000; color: #0f0; border: 1px solid #333;',
                'placeholder': 'NOTAS DE INTELIGÊNCIA...'
            }),
        }