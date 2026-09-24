TAX_RATE = 0.18


def price(amount):
    return amount * (1 + TAX_RATE)
