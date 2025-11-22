from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from .models import Group, GroupMember, SharedExpense, ExpenseSplit, Category
from .forms import GroupForm, SharedExpenseForm


@login_required
def group_list(request):
    """Display list of user's groups"""
    user_groups = request.user.user_groups.all()
    created_groups = request.user.created_groups.all()
    
    context = {
        'user_groups': user_groups,
        'created_groups': created_groups,
    }
    return render(request, 'expenses/group_list.html', context)


@login_required
def group_create(request):
    """Create a new group"""
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            
            # Add creator as admin member
            GroupMember.objects.create(
                group=group,
                user=request.user,
                is_admin=True
            )
            
            messages.success(request, f'Group "{group.name}" created successfully!')
            return redirect('group_detail', pk=group.pk)
    else:
        form = GroupForm()
    
    return render(request, 'expenses/group_form.html', {'form': form, 'action': 'Create'})


@login_required
def group_detail(request, pk):
    """Display group details and shared expenses"""
    group = get_object_or_404(Group, pk=pk)
    
    # Check if user is a member
    if not group.members.filter(id=request.user.id).exists():
        messages.error(request, 'You are not a member of this group.')
        return redirect('group_list')
    
    shared_expenses = group.shared_expenses.all().select_related('paid_by', 'category')
    
    # Calculate balances
    balances = {}
    for member in group.members.all():
        paid_total = shared_expenses.filter(paid_by=member).aggregate(
            total=Sum('amount'))['total'] or 0
        
        owed_total = ExpenseSplit.objects.filter(
            expense__group=group, user=member
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        balances[member.username] = paid_total - owed_total
    
    context = {
        'group': group,
        'shared_expenses': shared_expenses,
        'balances': balances,
        'is_admin': GroupMember.objects.filter(
            group=group, user=request.user, is_admin=True
        ).exists()
    }
    return render(request, 'expenses/group_detail.html', context)


@login_required
def group_join(request, pk):
    """Join a group via invitation or request"""
    group = get_object_or_404(Group, pk=pk)
    
    if group.members.filter(id=request.user.id).exists():
        messages.info(request, 'You are already a member of this group.')
    else:
        GroupMember.objects.create(group=group, user=request.user)
        messages.success(request, f'You have joined "{group.name}"!')
    
    return redirect('group_detail', pk=group.pk)


@login_required
def group_leave(request, pk):
    """Leave a group"""
    group = get_object_or_404(Group, pk=pk)
    membership = get_object_or_404(GroupMember, group=group, user=request.user)
    
    if request.method == 'POST':
        # Check if user has unsettled expenses
        unsettled = ExpenseSplit.objects.filter(
            expense__group=group, user=request.user, is_settled=False
        ).exists()
        
        if unsettled:
            messages.error(request, 'You cannot leave the group with unsettled expenses.')
            return redirect('group_detail', pk=group.pk)
        
        membership.delete()
        messages.success(request, f'You have left "{group.name}".')
        return redirect('group_list')
    
    return render(request, 'expenses/group_leave_confirm.html', {'group': group})


@login_required
def shared_expense_create(request, group_pk):
    """Create a shared expense for a group"""
    group = get_object_or_404(Group, pk=group_pk)
    
    # Check if user is a member
    if not group.members.filter(id=request.user.id).exists():
        messages.error(request, 'You are not a member of this group.')
        return redirect('group_list')
    
    if request.method == 'POST':
        form = SharedExpenseForm(request.POST, group=group)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.group = group
            expense.paid_by = request.user
            expense.save()
            
            # Create expense splits
            if expense.split_type == 'equal':
                # Split equally among all members
                member_count = group.members.count()
                split_amount = expense.amount / member_count
                
                for member in group.members.all():
                    ExpenseSplit.objects.create(
                        expense=expense,
                        user=member,
                        amount=split_amount
                    )
            
            messages.success(request, 'Shared expense added successfully!')
            return redirect('group_detail', pk=group.pk)
    else:
        form = SharedExpenseForm(group=group)
    
    context = {
        'form': form,
        'group': group,
        'action': 'Add'
    }
    return render(request, 'expenses/shared_expense_form.html', context)


@login_required
def shared_expense_detail(request, pk):
    """View shared expense details and splits"""
    expense = get_object_or_404(SharedExpense, pk=pk)
    
    # Check if user is a member of the group
    if not expense.group.members.filter(id=request.user.id).exists():
        messages.error(request, 'You are not a member of this group.')
        return redirect('group_list')
    
    splits = expense.splits.all().select_related('user')
    
    context = {
        'expense': expense,
        'splits': splits,
    }
    return render(request, 'expenses/shared_expense_detail.html', context)


@login_required
def settle_expense(request, split_pk):
    """Mark an expense split as settled"""
    split = get_object_or_404(ExpenseSplit, pk=split_pk, user=request.user)
    
    if request.method == 'POST':
        split.is_settled = True
        split.settled_at = timezone.now()
        split.save()
        
        messages.success(request, 'Expense marked as settled!')
        return redirect('group_detail', pk=split.expense.group.pk)
    
    return render(request, 'expenses/settle_expense_confirm.html', {'split': split})


@login_required
def group_members(request, pk):
    """Manage group members"""
    group = get_object_or_404(Group, pk=pk)
    
    # Check if user is admin
    is_admin = GroupMember.objects.filter(
        group=group, user=request.user, is_admin=True
    ).exists()
    
    if not is_admin:
        messages.error(request, 'Only group admins can manage members.')
        return redirect('group_detail', pk=group.pk)
    
    members = GroupMember.objects.filter(group=group).select_related('user')
    
    context = {
        'group': group,
        'members': members,
    }
    return render(request, 'expenses/group_members.html', context)


@login_required
def add_group_member(request, pk):
    """Add a member to the group"""
    group = get_object_or_404(Group, pk=pk)
    
    # Check if user is admin
    is_admin = GroupMember.objects.filter(
        group=group, user=request.user, is_admin=True
    ).exists()
    
    if not is_admin:
        messages.error(request, 'Only group admins can add members.')
        return redirect('group_detail', pk=group.pk)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            if group.members.filter(id=user.id).exists():
                messages.error(request, f'{username} is already a member.')
            else:
                GroupMember.objects.create(group=group, user=user)
                messages.success(request, f'{username} added to the group!')
        except User.DoesNotExist:
            messages.error(request, f'User "{username}" not found.')
    
    return redirect('group_members', pk=group.pk)