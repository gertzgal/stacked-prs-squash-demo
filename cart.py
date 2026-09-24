TAX_RATE = 0.17


def total(items, discount_pct=0):
    subtotal = sum(i["price"] for i in items)
    subtotal *= 1 - discount_pct
    return round(subtotal * (1 + TAX_RATE), 2)
