from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm


def expense_list(request):
    """
    Display a list of all expenses with summary statistics.
    """
    expenses = Expense.objects.all().select_related('category')
    categories = Category.objects.all()
    
    # Calculate total expenses
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    # Get expenses by category
    expenses_by_category = expenses.values('category__name').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    context = {
        'expenses': expenses,
        'categories': categories,
        'total_amount': total_amount,
        'expenses_by_category': expenses_by_category,
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
