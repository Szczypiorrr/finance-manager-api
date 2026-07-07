from app.exceptions.common_exceptions import InvalidAmount

def validate_amount(amount):
    """Checks if amount is greater than zero."""
    if amount <= 0:
        raise InvalidAmount()