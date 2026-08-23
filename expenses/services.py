from collections import defaultdict
from .models import Expense, ExpenseSplit
from .models import Expense, ExpenseSplit, Settlement
from decimal import Decimal

def calculate_group_balances(group):
    """
    برمی‌گردونه یه دیکشنری: {user: net_balance}
    اگه net_balance مثبت باشه یعنی طلبکاره (باید بهش بدن)
    اگه منفی باشه یعنی بدهکاره (باید بده)
    """
    balances = defaultdict(lambda: 0)

    expenses = Expense.objects.filter(group=group).select_related('paid_by')
    for expense in expenses:
        balances[expense.paid_by] += expense.amount

    splits = ExpenseSplit.objects.filter(expense__group=group).select_related('user')
    for split in splits:
        balances[split.user] -= split.amount

    settlements = Settlement.objects.filter(group=group).select_related('paid_by', 'paid_to')
    for settlement in settlements:
        balances[settlement.paid_by] += settlement.amount
        balances[settlement.paid_to] -= settlement.amount

    return dict(balances)


def simplify_debts(balances):
    """
    ورودی: دیکشنری {user: net_balance}
    خروجی: لیستی از تراکنش‌های پیشنهادی [{'from': user, 'to': user, 'amount': ...}]
    """
    creditors = []
    debtors = []

    for user, balance in balances.items():
        if balance > 0:
            creditors.append([user, balance])
        elif balance < 0:
            debtors.append([user, -balance])

    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    transactions = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        debtor, debt_amount = debtors[i]
        creditor, credit_amount = creditors[j]

        payment = min(debt_amount, credit_amount)

        transactions.append({
            'from': debtor,
            'to': creditor,
            'amount': payment,
        })

        debtors[i][1] -= payment
        creditors[j][1] -= payment

        ZERO = Decimal('0.00')
        # توی simplify_debts جایی که == 0 داری:
        if debtors[i][1] <= ZERO:
            i += 1
        if creditors[j][1] <= ZERO:
            j += 1

    return transactions