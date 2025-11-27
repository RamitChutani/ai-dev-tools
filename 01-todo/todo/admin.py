from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'due_date', 'created_at')
    list_filter = ('completed', 'created_at', 'due_date')
    search_fields = ('title', 'description')
    list_editable = ('completed',)
    date_hierarchy = 'created_at'
