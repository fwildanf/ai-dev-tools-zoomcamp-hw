from django.contrib import admin
from .models import Todo, Category


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """Admin configuration for Todo model."""
    list_display = ['title', 'user', 'category', 'completed', 'created_at', 'due_date']
    list_filter = ['completed', 'category', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'user')
        }),
        ('Organization', {
            'fields': ('category',)
        }),
        ('Status', {
            'fields': ('completed',)
        }),
        ('Dates', {
            'fields': ('due_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
