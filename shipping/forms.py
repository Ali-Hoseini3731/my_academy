from django import forms
from django.core.exceptions import ValidationError

from lib.validation import len_zipcode
from shipping.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    # zipcode = forms.CharField(validators=[len_zipcode])

    class Meta:
        model = ShippingAddress
        fields = ["city", "zipcode", "address", "number"]

    def clean_zipcode(self):
        zipcode = self.cleaned_data["zipcode"]
        if len(zipcode) <= 2:
            raise ValidationError("The Length must be greater than 2 !")

        return zipcode

    # def clean(self):
    #     cleaned_data = super().clean()
    #     zipcode = cleaned_data["zipcode"]
    #     if len(zipcode) <= 2:
    #         raise ValidationError("The Length must be greater than 2 !")
    #     return cleaned_data
