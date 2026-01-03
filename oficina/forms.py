from django import forms
from .models import Cliente, Veiculo, Servico

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone']

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        # 'obs_gerais' deve estar na lista abaixo
        fields = ['cliente', 'modelo', 'placa', 'foto_carro', 'obs_gerais']
        widgets = {
            'obs_gerais': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Manutenção preventiva pendente...'}),
        }

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['veiculo', 'descricao', 'foto_local_servico']