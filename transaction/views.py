from django.http import HttpResponse

from transaction.models import Transaction


def transaction_list(request):
    transactions = Transaction.objects.select_related("user").all()
    context = [
        f"{transaction.user.username}---{transaction.get_transaction_type_display()}---{transaction.amount}<br>"
        for transaction in transactions
    ]
    return HttpResponse(context)
