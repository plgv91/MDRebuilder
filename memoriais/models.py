from django.db import models

OPCOES = [
    ('Bom', 'Bom'),
    ('Regular', 'Regular'),
    ('Ruim', 'Ruim')
]

class Comentario(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=150, null=False, blank=False)
    opiniao = models.CharField(max_length=7, null=False, blank=False, choices=OPCOES, default='Bom')
    mensagem = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome
