from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def multiplicar(cantidad, precio):
    """Multiplica cantidad * precio usando Decimal (acepta '100.00')."""
    try:
        return (Decimal(str(cantidad)) * Decimal(str(precio))).quantize(Decimal('0.01'))
    except (InvalidOperation, ValueError, TypeError):
        return ''