from django import forms

from lib.validation import len_zipcode
from shipping.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    zipcode = forms.CharField(validators=[len_zipcode])

    class Meta:
        model = ShippingAddress
        fields = ("city", "zipcode", "address", "number")
