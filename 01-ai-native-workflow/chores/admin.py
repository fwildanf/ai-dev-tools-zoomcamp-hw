from django.contrib import admin

from .models import Chore, HouseholdMember


@admin.register(HouseholdMember)
class HouseholdMemberAdmin(admin.ModelAdmin):
	list_display = ['name', 'created_at']
	search_fields = ['name']


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
	list_display = ['name', 'assignee', 'due_date', 'frequency', 'completed']
	list_filter = ['frequency', 'completed', 'assignee']
	search_fields = ['name']
