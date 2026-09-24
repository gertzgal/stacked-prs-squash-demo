# layer A adds a tax rate
TAX_RATE = 0.17


def price(amount):
    return amount * (1 + TAX_RATE)
