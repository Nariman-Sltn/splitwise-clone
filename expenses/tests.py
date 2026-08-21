from django.test import TestCase
from django.contrib.auth.models import User
from .models import Group, GroupMembership, Expense, ExpenseSplit, Settlement
from .services import calculate_group_balances, simplify_debts
from decimal import Decimal


class CalculateGroupBalancesTest(TestCase):

    def setUp(self):
        # Arrange — داده‌های مشترک بین همه تست‌ها
        self.ali = User.objects.create_user(username='ali', password='test')
        self.reza = User.objects.create_user(username='reza', password='test')

        self.group = Group(name='تست', created_by=self.ali)
        self.group.set_password('1234')
        self.group.save()

        GroupMembership.objects.create(group=self.group, user=self.ali)
        GroupMembership.objects.create(group=self.group, user=self.reza)

    def test_simple_expense(self):
        # علی ۱۰۰ تومن میده، هر دو سهیمن
        expense = Expense.objects.create(
            group=self.group,
            title='شام',
            amount=Decimal('100.00'),
            paid_by=self.ali,
        )
        ExpenseSplit.objects.create(expense=expense, user=self.ali, amount=Decimal('50.00'))
        ExpenseSplit.objects.create(expense=expense, user=self.reza, amount=Decimal('50.00'))

        # Act
        balances = calculate_group_balances(self.group)

        # Assert
        self.assertEqual(balances[self.ali], Decimal('50.00'))
        self.assertEqual(balances[self.reza], Decimal('-50.00'))

    def test_settlement_reduces_debt(self):
        # علی ۱۰۰ تومن میده، هر دو سهیمن
        expense = Expense.objects.create(
            group=self.group,
            title='شام',
            amount=Decimal('100.00'),
            paid_by=self.ali,
        )
        ExpenseSplit.objects.create(expense=expense, user=self.ali, amount=Decimal('50.00'))
        ExpenseSplit.objects.create(expense=expense, user=self.reza, amount=Decimal('50.00'))

        # رضا ۳۰ تومن تسویه می‌کنه
        Settlement.objects.create(
            group=self.group,
            paid_by=self.reza,
            paid_to=self.ali,
            amount=Decimal('30.00'),
        )

        balances = calculate_group_balances(self.group)

        self.assertEqual(balances[self.ali], Decimal('20.00'))
        self.assertEqual(balances[self.reza], Decimal('-20.00'))

    def test_full_settlement_clears_debt(self):
        # علی ۱۰۰ تومن میده، هر دو سهیمن
        expense = Expense.objects.create(
            group=self.group,
            title='شام',
            amount=Decimal('100.00'),
            paid_by=self.ali,
        )
        ExpenseSplit.objects.create(expense=expense, user=self.ali, amount=Decimal('50.00'))
        ExpenseSplit.objects.create(expense=expense, user=self.reza, amount=Decimal('50.00'))

        # رضا کل بدهیش رو میده
        Settlement.objects.create(
            group=self.group,
            paid_by=self.reza,
            paid_to=self.ali,
            amount=Decimal('50.00'),
        )

        balances = calculate_group_balances(self.group)

        self.assertEqual(balances[self.ali], Decimal('0.00'))
        self.assertEqual(balances[self.reza], Decimal('0.00'))

class SimplifyDebtsTest(TestCase):

    def test_simple_two_person_debt(self):
        ali = User.objects.create_user(username='ali', password='test')
        reza = User.objects.create_user(username='reza', password='test')

        balances = {
            ali: Decimal('50.00'),
            reza: Decimal('-50.00'),
        }

        transactions = simplify_debts(balances)

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['from'], reza)
        self.assertEqual(transactions[0]['to'], ali)
        self.assertEqual(transactions[0]['amount'], Decimal('50.00'))

    def test_three_person_simplification(self):
        ali = User.objects.create_user(username='ali', password='test')
        reza = User.objects.create_user(username='reza', password='test')
        sara = User.objects.create_user(username='sara', password='test')

        balances = {
            ali: Decimal('100.00'),
            reza: Decimal('-60.00'),
            sara: Decimal('-40.00'),
        }

        transactions = simplify_debts(balances)

        # باید دو تراکنش باشه — رضا و سارا هر کدوم به علی بدن
        self.assertEqual(len(transactions), 2)