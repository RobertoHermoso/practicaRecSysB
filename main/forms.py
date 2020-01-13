from django import forms
 
class UsuarioForm(forms.Form):
    usuario = forms.CharField(label='Id del usuario', max_length=100)

class GeneroForm(forms.Form):
    genero = forms.CharField(label='Genero', max_length=100)