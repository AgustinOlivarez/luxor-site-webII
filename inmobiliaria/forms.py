from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre',
            'class': 'input-form'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Tu correo',
            'class': 'input-form'
        })
    )
    asunto = forms.CharField(
        label="Asunto",
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Asunto',
            'class': 'input-form'
        })
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe tu mensaje...',
            'class': 'textarea-form',
            'rows': 5
        })
    )
    fecha = forms.DateField(
        label="Fecha tentativa",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'input-form'
        })
    )
    categoria = forms.CharField(
        widget=forms.HiddenInput(), required=False)
class RegistroForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=100)
    last_name = forms.CharField(label="Apellido", max_length=100)
    email = forms.EmailField(label="Correo electrónico")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        # El email pasa a ser su username
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user