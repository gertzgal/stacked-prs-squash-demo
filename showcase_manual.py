# layer A adds a tax rate
TAX_RATE = 0.18  # layer B: new rate


def price(amount):
    return round(amount * (1 + TAX_RATE), 2)


def price_with_discount(amount, pct):
    return price(amount * (1 - pct))
