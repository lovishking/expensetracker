# Generated migration for adding user fields

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def assign_default_user(apps, schema_editor):
    """Assign existing records to the first superuser"""
    User = apps.get_model('auth', 'User')
    Category = apps.get_model('expenses', 'Category')
    Expense = apps.get_model('expenses', 'Expense')
    
    # Get the first user (superuser we just created)
    try:
        default_user = User.objects.filter(is_superuser=True).first()
        if not default_user:
            default_user = User.objects.first()
        
        if default_user:
            # Assign all categories to default user
            Category.objects.filter(user__isnull=True).update(user=default_user)
            # Assign all expenses to default user
            Expense.objects.filter(user__isnull=True).update(user=default_user)
    except Exception:
        pass  # Handle case where no users exist


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expenses', '0001_initial'),
    ]

    operations = [
        # Add user field to Category as nullable first
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
        # Add user field to Expense as nullable first
        migrations.AddField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL),
        ),
        # Run the data migration
        migrations.RunPython(assign_default_user),
        # Make fields non-nullable
        migrations.AlterField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL),
        ),
        # Remove unique constraint on category name alone and add unique_together
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'user')},
        ),
    ]