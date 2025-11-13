from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
import json
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm


def expense_list(request):
    """
    Display a list of all expenses with summary statistics.
    Supports filtering by time period: daily, weekly, monthly, or all.
    """
    # Get filter parameter from request
    time_filter = request.GET.get('period', 'all')
    
    # Base queryset
    expenses = Expense.objects.all().select_related('category')
    
    # Apply time filter
    now = timezone.now()
    if time_filter == 'daily':
        start_date = now.date()
        expenses = expenses.filter(date=start_date)
        period_label = "Today"
    elif time_filter == 'weekly':
        start_date = now.date() - timedelta(days=now.weekday())  # Start of current week (Monday)
        expenses = expenses.filter(date__gte=start_date)
        period_label = "This Week"
    elif time_filter == 'monthly':
        start_date = now.date().replace(day=1)  # Start of current month
        expenses = expenses.filter(date__gte=start_date)
        period_label = "This Month"
    else:
        period_label = "All Time"
    
    categories = Category.objects.all()
    
    # Calculate total expenses for the filtered period
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    # Get expenses by category for the filtered period
    expenses_by_category = expenses.values('category__name').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Prepare data for pie chart (category breakdown)
    category_labels = [item['category__name'] for item in expenses_by_category]
    category_data = [float(item['total']) for item in expenses_by_category]
    
    # Convert queryset to list to avoid SQLite issues with iteration
    expenses_list = list(expenses)
    
    # Prepare data for line chart (spending over time)
    trend_labels = []
    trend_amounts = []
    
    if time_filter == 'daily':
        # For daily view, show just today's total
        trend_labels = ['Today']
        trend_amounts = [float(total_amount)]
    elif time_filter == 'weekly':
        # Show daily breakdown for the week - group by date in Python
        daily_totals = defaultdict(float)
        for expense in expenses_list:
            daily_totals[expense.date] += float(expense.amount)
        
        # Sort by date and format
        sorted_dates = sorted(daily_totals.keys())
        trend_labels = [d.strftime('%a') for d in sorted_dates]
        trend_amounts = [daily_totals[d] for d in sorted_dates]
    elif time_filter == 'monthly':
        # Show daily breakdown for the month - group by date in Python
        daily_totals = defaultdict(float)
        for expense in expenses_list:
            daily_totals[expense.date] += float(expense.amount)
        
        # Sort by date and format
        sorted_dates = sorted(daily_totals.keys())
        trend_labels = [d.strftime('%b %d') for d in sorted_dates]
        trend_amounts = [daily_totals[d] for d in sorted_dates]
    else:
        # Show monthly breakdown for all time - group by month in Python
        monthly_totals = defaultdict(float)
        for expense in expenses_list:
            month_key = expense.date.replace(day=1)  # First day of month
            monthly_totals[month_key] += float(expense.amount)
        
        # Sort by date and format
        sorted_months = sorted(monthly_totals.keys())
        trend_labels = [m.strftime('%b %Y') for m in sorted_months]
        trend_amounts = [monthly_totals[m] for m in sorted_months]
    
    context = {
        'expenses': expenses,
        'categories': categories,
        'total_amount': total_amount,
        'expenses_by_category': expenses_by_category,
        'time_filter': time_filter,
        'period_label': period_label,
        # Chart data
        'category_labels_json': json.dumps(category_labels),
        'category_data_json': json.dumps(category_data),
        'trend_labels_json': json.dumps(trend_labels),
        'trend_amounts_json': json.dumps(trend_amounts),
    }
    return render(request, 'expenses/expense_list.html', context)


def expense_create(request):
    """
    Create a new expense.
    """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    
    return render(request, 'expenses/expense_form.html', {'form': form, 'action': 'Add'})


def expense_update(request, pk):
    """
    Update an existing expense.
    """
    expense = get_object_or_404(Expense, pk=pk)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expenses/expense_form.html', {'form': form, 'action': 'Update'})


def expense_delete(request, pk):
    """
    Delete an expense.
    """
    expense = get_object_or_404(Expense, pk=pk)
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')
    
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


def category_list(request):
    """
    Display a list of all categories.
    """
    categories = Category.objects.annotate(
        expense_count=Count('expenses'),
        total_amount=Sum('expenses__amount')
    )
    
    context = {
        'categories': categories,
    }
    return render(request, 'expenses/category_list.html', context)


def category_create(request):
    """
    Create a new category.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'expenses/category_form.html', {'form': form, 'action': 'Add'})


def category_update(request, pk):
    """
    Update an existing category.
    """
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'expenses/category_form.html', {'form': form, 'action': 'Update'})


def category_delete(request, pk):
    """
    Delete a category.
    """
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'expenses/category_confirm_delete.html', {'category': category})
