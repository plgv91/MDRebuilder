from django.forms import ModelForm
from memoriais.models import Comentario

class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['nome', 'email', 'opiniao', 'mensagem']
