from exceptions.common_exceptions import InvalidAmount

def validate_amount(amount):
    if amount <= 0:
        raise InvalidAmount()