
"""Formularios de la app clientes — W08."""

from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    """Formulario para crear y editar clientes."""

    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'activo']

        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'erp-input',
                    'placeholder': 'Nombre completo o razón social',
                }
            ),
            'correo': forms.EmailInput(
                attrs={
                    'class': 'erp-input',
                    'placeholder': 'correo@ejemplo.com',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'erp-input',
                    'placeholder': '461 123 4567',
                }
            ),
        }

    def clean_correo(self):
        """Evita registrar un correo que ya pertenece a otro cliente."""

        correo = self.cleaned_data.get('correo')

        consulta = Cliente.objects.filter(correo__iexact=correo)

        if self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():
            raise forms.ValidationError(
                'Este correo ya existe.'
            )

        return correo
