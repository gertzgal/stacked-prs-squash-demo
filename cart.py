TAX_RATE = 0.17


def total(items):
    subtotal = sum(i["price"] for i in items)
    return round(subtotal * (1 + TAX_RATE), 2)
