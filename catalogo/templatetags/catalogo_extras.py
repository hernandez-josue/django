from decimal import Decimal, ROUND_HALF_UP

from django import template

register = template.Library()


@register.filter
def mul(a, b):
    """Multiplica dos valores con 2 decimales (cantidad * precio)."""
    try:
        r = Decimal(str(a)) * Decimal(str(b))
        return r.quantize(Decimal('0.01'), ROUND_HALF_UP)
    except Exception:
        return ''