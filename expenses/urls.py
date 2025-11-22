from django.urls import path
from . import views
from . import auth_views
from . import group_views

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.login_view, name='login'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Expense URLs
    path('', views.expense_list, name='expense_list'),
    path('expense/add/', views.expense_create, name='expense_create'),
    path('expense/<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('expense/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('category/add/', views.category_create, name='category_create'),
    path('category/<int:pk>/edit/', views.category_update, name='category_update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Group URLs
    path('groups/', group_views.group_list, name='group_list'),
    path('groups/create/', group_views.group_create, name='group_create'),
    path('groups/<int:pk>/', group_views.group_detail, name='group_detail'),
    path('groups/<int:pk>/join/', group_views.group_join, name='group_join'),
    path('groups/<int:pk>/leave/', group_views.group_leave, name='group_leave'),
    path('groups/<int:pk>/members/', group_views.group_members, name='group_members'),
    path('groups/<int:pk>/add-member/', group_views.add_group_member, name='add_group_member'),
    
    # Shared Expense URLs
    path('groups/<int:group_pk>/expense/add/', group_views.shared_expense_create, name='shared_expense_create'),
    path('shared-expense/<int:pk>/', group_views.shared_expense_detail, name='shared_expense_detail'),
    path('expense-split/<int:split_pk>/settle/', group_views.settle_expense, name='settle_expense'),
]
