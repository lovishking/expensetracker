from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from .models import Category, Expense


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Food',
            description='Food and groceries'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Food')
        self.assertEqual(str(self.category), 'Food')


class ExpenseModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Transportation')
        self.expense = Expense.objects.create(
            title='Uber ride',
            amount=Decimal('25.50'),
            category=self.category,
            description='Trip to office'
        )

    def test_expense_creation(self):
        self.assertEqual(self.expense.title, 'Uber ride')
        self.assertEqual(self.expense.amount, Decimal('25.50'))
        self.assertEqual(self.expense.category, self.category)
        self.assertIn('Uber ride', str(self.expense))
