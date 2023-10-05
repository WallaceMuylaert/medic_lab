from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Criar tabela de tipo de exames no banco de dados
class TiposExames(models.Model):
    nome = models.CharField(max_length=50)
    tipos_choices = (
        ('I', 'Exame de Imagem'),
        ('S', 'Exame de Sangue')
    )
    tipo = models.CharField(max_length=1, choices=tipos_choices) #Passando "tipos_coices"
    preco = models.FloatField() 
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.TimeField(auto_now=False, auto_now_add=False)
    horario_final = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self) -> str:
        return self.nome
    
class SolicitacaoExame(models.Model):
    choice_status = (
    ('E', 'Em análise'),
    ('F', 'Finalizado')
    )
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING) #ForeignKey -> chave estangeira 
    exame = models.ForeignKey(TiposExames, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True) #FileField -> recebendo arquivo
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)
    
    def __str__(self):
       return f'{self.usuario} | {self.exame.nome}'
    
    def badge_template(self):
        if self.status == 'E':
            classes_css = 'bg-warning text-dark'
            texto = "Em análise"
        elif self.status == 'F':
            classes_css = 'bg-success'
            texto = "Finalizado"
        
        return mark_safe(f"<span class='badge bg-primary {classes_css}'>{texto}</span>")
    
class PedidosExames(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exames = models.ManyToManyField(SolicitacaoExame) #ManyToManyField -> Relação de N para N
    agendado = models.BooleanField(default=True)
    data = models.DateField()
    def __str__(self):
        return f'{self.usuario} | {self.data}'