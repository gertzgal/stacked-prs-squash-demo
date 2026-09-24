TAX_RATE = 0.17
FREE_SHIPPING_OVER = 200
SHIPPING_FEE = 15


def total(items, discount_pct=0):
    subtotal = sum(i["price"] for i in items)
    subtotal *= 1 - discount_pct
    shipping = 0 if subtotal >= FREE_SHIPPING_OVER else SHIPPING_FEE
    return round(subtotal * (1 + TAX_RATE) + shipping, 2)
