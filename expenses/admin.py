from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from .models import Category, Expense, Group, GroupMember, SharedExpense, ExpenseSplit


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'description', 'expense_count', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username']
    ordering = ['user', 'name']
    
    def expense_count(self, obj):
        return obj.expenses.count()
    expense_count.short_description = 'Number of Expenses'


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'user', 'category', 'date', 'created_at']
    list_filter = ['user', 'category', 'date', 'created_at']
    search_fields = ['title', 'description', 'user__username', 'category__name']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    actions = ['export_user_expenses', 'delete_selected_expenses']
    
    # Group expenses by user in the changelist
    list_select_related = ['user', 'category']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'category')
    
    def export_user_expenses(self, request, queryset):
        """Export selected expenses as CSV"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['User', 'Title', 'Amount', 'Category', 'Date', 'Description'])
        
        for expense in queryset:
            writer.writerow([
                expense.user.username,
                expense.title,
                expense.amount,
                expense.category.name,
                expense.date,
                expense.description
            ])
        
        return response
    export_user_expenses.short_description = "Export selected expenses as CSV"
    
    def delete_selected_expenses(self, request, queryset):
        """Delete selected expenses with confirmation"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Successfully deleted {count} expenses.')
    delete_selected_expenses.short_description = "Delete selected expenses"


# Add a custom admin view to show user expense summaries
class UserExpenseSummaryAdmin(admin.ModelAdmin):
    """Custom admin to show expense summaries by user"""
    change_list_template = 'admin/user_expense_summary.html'
    
    def changelist_view(self, request, extra_context=None):
        # Get summary data for each user
        user_summaries = []
        for user in User.objects.all():
            total_expenses = Expense.objects.filter(user=user).aggregate(
                total_amount=Sum('amount'),
                total_count=Count('id')
            )
            user_summaries.append({
                'user': user,
                'total_amount': total_expenses['total_amount'] or 0,
                'total_count': total_expenses['total_count'] or 0,
                'categories_count': Category.objects.filter(user=user).count()
            })
        
        extra_context = extra_context or {}
        extra_context['user_summaries'] = user_summaries
        
        return super().changelist_view(request, extra_context)


# Register a proxy model for the summary view
class UserExpenseSummary(User):
    class Meta:
        proxy = True
        verbose_name = 'User Expense Summary'
        verbose_name_plural = 'User Expense Summaries'

admin.site.register(UserExpenseSummary, UserExpenseSummaryAdmin)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'member_count', 'total_expenses', 'created_at']
    list_filter = ['created_by', 'created_at']
    search_fields = ['name', 'created_by__username']
    ordering = ['-created_at']
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'
    
    def total_expenses(self, obj):
        total = obj.shared_expenses.aggregate(total=Sum('amount'))['total'] or 0
        return f'${total:.2f}'
    total_expenses.short_description = 'Total Expenses'


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'is_admin', 'joined_at']
    list_filter = ['is_admin', 'joined_at', 'group']
    search_fields = ['user__username', 'group__name']
    ordering = ['-joined_at']


@admin.register(SharedExpense)
class SharedExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'group', 'paid_by', 'split_type', 'date', 'created_at']
    list_filter = ['group', 'paid_by', 'split_type', 'date', 'created_at']
    search_fields = ['title', 'description', 'group__name', 'paid_by__username']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']


@admin.register(ExpenseSplit)
class ExpenseSplitAdmin(admin.ModelAdmin):
    list_display = ['expense', 'user', 'amount', 'is_settled', 'settled_at']
    list_filter = ['is_settled', 'settled_at', 'expense__group']
    search_fields = ['expense__title', 'user__username', 'expense__group__name']
    ordering = ['-expense__date', 'user__username']
