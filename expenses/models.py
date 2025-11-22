from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Category model for organizing expenses.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = ['name', 'user']  # Allow same category name for different users

    def __str__(self):
        return self.name


class Expense(models.Model):
    """
    Expense model for tracking individual expenses.
    """
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses')
    description = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - ${self.amount}"


class Group(models.Model):
    """
    Group model for shared expenses among multiple users.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, through='GroupMember', related_name='user_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_member_count(self):
        return self.members.count()

    def get_total_expenses(self):
        return self.shared_expenses.aggregate(total=models.Sum('amount'))['total'] or 0


class GroupMember(models.Model):
    """
    Through model for Group-User relationship with additional fields.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ['group', 'user']

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class SharedExpense(models.Model):
    """
    Model for expenses shared among group members.
    """
    SPLIT_CHOICES = [
        ('equal', 'Split Equally'),
        ('exact', 'Exact Amounts'),
        ('percentage', 'By Percentage'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='shared_expenses')
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_expenses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='shared_expenses', null=True, blank=True)
    date = models.DateField(default=timezone.now)
    split_type = models.CharField(max_length=20, choices=SPLIT_CHOICES, default='equal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - ${self.amount} ({self.group.name})"

    def get_split_amount_per_person(self):
        """Calculate split amount per person for equal split"""
        if self.split_type == 'equal':
            member_count = self.group.get_member_count()
            if member_count > 0:
                return self.amount / member_count
        return 0

    def get_user_share(self, user):
        """Get a specific user's share of this expense"""
        try:
            split = ExpenseSplit.objects.get(expense=self, user=user)
            return split.amount
        except ExpenseSplit.DoesNotExist:
            if self.split_type == 'equal':
                return self.get_split_amount_per_person()
            return 0


class ExpenseSplit(models.Model):
    """
    Model to track how much each user owes for a shared expense.
    """
    expense = models.ForeignKey(SharedExpense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_splits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_settled = models.BooleanField(default=False)
    settled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['expense', 'user']

    def __str__(self):
        return f"{self.user.username} owes ${self.amount} for {self.expense.title}"
