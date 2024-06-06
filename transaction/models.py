from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce


class Transaction(models.Model):
    CHARGE = 1
    PURCHASE = 2
    RECEIVED_TRANSFER = 3
    SENT_TRANSFER = 4
    TRANSACTION_TYPE_FILED = (
        (CHARGE, "Charge"),
        (PURCHASE, "Purchase"),
        (RECEIVED_TRANSFER, "Received Transfer"),
        (SENT_TRANSFER, "Sent Transfer"),
    )

    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="transactions")
    transaction_type = models.PositiveSmallIntegerField(default=CHARGE, choices=TRANSACTION_TYPE_FILED)
    amount = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}---{self.get_transaction_type_display()}----{self.amount}"

    @classmethod
    def get_report(cls):
        positive_amount = Sum("transactions__amount", filter=Q(transactions__transaction_type__in=[1, 3]))
        negative_amount = Sum("transactions__amount", filter=Q(transactions__transaction_type__in=[2, 4]))
        users = User.objects.all().annotate(
            transactions_count=Count("transactions__id"),
            balance=Coalesce(positive_amount, 0) - Coalesce(negative_amount, 0)
        )
        return users

    @classmethod
    def total_balance(cls):
        queryset = cls.get_report()
        return queryset.aggregate(total=Sum("balance"))

    @classmethod
    def user_balance(cls, user):
        positive_amount = Sum("amount", filter=Q(transaction_type__in=[1, 3]))
        negative_amount = Sum("amount", filter=Q(transaction_type__in=[2, 4]))
        user_balance = user.transactions.all().aggregate(
            balance=Coalesce(positive_amount, 0) - Coalesce(negative_amount, 0)
        )
        return user_balance.get("balance", 0)


class UserBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="record_balances")
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}---{self.balance}---{self.created_time}"

    @classmethod
    def record_user_balance(cls, user):
        instance = cls.objects.create(user=user, balance=Transaction.user_balance(user))
        return instance

    @classmethod
    def record_all_users_balance(cls):
        for user in User.objects.all():
            cls.record_user_balance(user)


class TransferTransaction(models.Model):
    sender_transaction = models.ForeignKey(
        Transaction, on_delete=models.RESTRICT, related_name="sent_transfers"
    )
    receiver_transaction = models.ForeignKey(
        Transaction, on_delete=models.RESTRICT, related_name="received_transfers"
    )

    def __str__(self):
        return f"{self.sender_transaction}------->{self.receiver_transaction}"

    @classmethod
    def transfer(cls, sender_transaction, receiver_transaction, amount):
        if Transaction.user_balance(sender_transaction) < amount:
            return "transfer is not allowed, insufficient balance"

        with transaction.atomic():
            sender_transaction = Transaction.objects.create(
                user=sender_transaction, transaction_type=Transaction.SENT_TRANSFER, amount=amount
            )
            receiver_transaction = Transaction.objects.create(
                user=receiver_transaction, transaction_type=Transaction.RECEIVED_TRANSFER, amount=amount
            )
            instance = cls.objects.create(
                sender_transaction=sender_transaction, receiver_transaction=receiver_transaction
            )

        return instance


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="scores")
    score = models.BigIntegerField()

    @classmethod
    def change_score(cls, user, score):
        # with transaction.atomic():
        #     try:
        #         instance = cls.objects.select_for_update().get(user=user)
        #     except User.DoesNotExist:
        #         instance = cls.objects.create(user=user, score=0)
        #     instance.score += score
        #     instance.save()

        # with transaction.atomic():
        #     instance = cls.objects.select_for_update().get(user=user)
        #     if not instance.exists():
        #         instance = cls.objects.create(user=user, score=0)
        #
        #     instance.score += score
        #     instance.save()

        with transaction.atomic():
            instance = cls.objects.select_for_update().filter(user=user)
            if not instance.exists():
                instance = cls.objects.create(user=user, score=0)
            else:
                instance = instance.first()
            instance.score += score
            instance.save()

