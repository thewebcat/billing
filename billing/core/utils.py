import decimal


def round_decimal(x):
    return x.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_UP)
