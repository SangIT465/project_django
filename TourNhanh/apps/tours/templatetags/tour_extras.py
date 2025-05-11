from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def split(value, delimiter):
    """
    Filter này chia một chuỗi thành danh sách các chuỗi nhỏ hơn
    Sử dụng: {{ value|split:'delimiter' }}
    """
    return value.split(delimiter)

@register.filter
def multiply(value, arg):
    """
    Filter này nhân một giá trị với một số
    Sử dụng: {{ value|multiply:0.7 }}
    """
    try:
        # Chuyển đổi arg thành Decimal nếu value là Decimal
        if isinstance(value, Decimal):
            return value * Decimal(str(arg))
        return value * arg
    except (ValueError, TypeError):
        return value
