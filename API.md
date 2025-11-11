# API Documentation

## Overview

This document describes the views and endpoints available in the Expense Tracker application.

## Expense Views

### Expense List

- **URL**: `/`
- **Name**: `expense_list`
- **Method**: GET
- **Description**: Display all expenses with summary statistics
- **Response**: Renders expense list with totals and category breakdown

### Create Expense

- **URL**: `/expense/add/`
- **Name**: `expense_create`
- **Methods**: GET, POST
- **Description**: Create a new expense
- **Form Fields**:
  - `title` (required): String, max 200 characters
  - `amount` (required): Decimal, max 10 digits, 2 decimal places
  - `category` (required): Foreign key to Category
  - `date` (required): Date field
  - `description` (optional): Text field

### Update Expense

- **URL**: `/expense/<int:pk>/edit/`
- **Name**: `expense_update`
- **Methods**: GET, POST
- **Description**: Update an existing expense
- **Parameters**: `pk` - Primary key of expense to update

### Delete Expense

- **URL**: `/expense/<int:pk>/delete/`
- **Name**: `expense_delete`
- **Methods**: GET, POST
- **Description**: Delete an expense
- **Parameters**: `pk` - Primary key of expense to delete

## Category Views

### Category List

- **URL**: `/categories/`
- **Name**: `category_list`
- **Method**: GET
- **Description**: Display all categories with expense counts and totals

### Create Category

- **URL**: `/category/add/`
- **Name**: `category_create`
- **Methods**: GET, POST
- **Description**: Create a new category
- **Form Fields**:
  - `name` (required): String, max 100 characters, unique
  - `description` (optional): Text field

### Update Category

- **URL**: `/category/<int:pk>/edit/`
- **Name**: `category_update`
- **Methods**: GET, POST
- **Description**: Update an existing category
- **Parameters**: `pk` - Primary key of category to update

### Delete Category

- **URL**: `/category/<int:pk>/delete/`
- **Name**: `category_delete`
- **Methods**: GET, POST
- **Description**: Delete a category (also deletes related expenses)
- **Parameters**: `pk` - Primary key of category to delete

## Admin Panel

- **URL**: `/admin/`
- **Description**: Django admin interface with full CRUD operations
- **Features**:
  - Search expenses by title and description
  - Filter expenses by category and date
  - Bulk actions
  - Date hierarchy navigation

## Response Formats

All views return HTML responses rendered with Django templates.

### Success Messages

- Uses Django's messages framework
- Bootstrap alert styling (success, danger, info, warning)

### Error Handling

- Form validation errors displayed inline
- 404 for non-existent resources
- Server errors shown with Django error pages (in DEBUG mode)

## Database Queries

### Optimizations

- `select_related('category')` for expense queries to reduce database hits
- `annotate()` for calculating statistics
- Proper indexing on foreign keys

## Template Context Variables

### expense_list.html

- `expenses`: QuerySet of all Expense objects
- `categories`: QuerySet of all Category objects
- `total_amount`: Sum of all expense amounts
- `expenses_by_category`: Annotated category data

### category_list.html

- `categories`: QuerySet with annotated expense_count and total_amount

## Forms

### ExpenseForm

- Bootstrap-styled form fields
- Client-side HTML5 validation
- Server-side Django validation

### CategoryForm

- Bootstrap-styled form fields
- Unique name validation
