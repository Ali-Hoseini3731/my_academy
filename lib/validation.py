from django.core.exceptions import ValidationError


def len_zipcode(value):
    if len(value) <= 2:
        raise ValidationError("Length of zipcode must be greater than or equal to 2!")
