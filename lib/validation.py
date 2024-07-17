from django.core.exceptions import ValidationError


def len_zipcode(value):
    if len(value) <= 2:
        raise ValidationError("The Length must be great than 2 !")
