from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ChoreForm, HouseholdMemberForm
from .models import Chore, HouseholdMember


def index(request):
	assignee_id = request.GET.get('assignee')
	chores = Chore.objects.select_related('assignee')
	if assignee_id:
		chores = chores.filter(assignee_id=assignee_id)
	return render(request, 'chores/index.html', {
		'chores': chores,
		'members': HouseholdMember.objects.all(),
		'selected_assignee': assignee_id or '',
	})


def member_create(request):
	form = HouseholdMemberForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Household member added.')
		return redirect('chores:index')
	return render(request, 'chores/member_form.html', {'form': form, 'title': 'Add member'})


def member_edit(request, pk):
	member = get_object_or_404(HouseholdMember, pk=pk)
	form = HouseholdMemberForm(request.POST or None, instance=member)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Household member updated.')
		return redirect('chores:index')
	return render(request, 'chores/member_form.html', {'form': form, 'title': 'Edit member'})


def member_delete(request, pk):
	member = get_object_or_404(HouseholdMember, pk=pk)
	if request.method == 'POST':
		member.delete()
		messages.success(request, 'Household member removed.')
		return redirect('chores:index')
	return render(request, 'chores/confirm_delete.html', {
		'object': member,
		'object_type': 'member',
		'cancel_url': 'chores:index',
	})


def chore_create(request):
	form = ChoreForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Chore created.')
		return redirect('chores:index')
	return render(request, 'chores/chore_form.html', {'form': form, 'title': 'Add chore'})


def chore_edit(request, pk):
	chore = get_object_or_404(Chore, pk=pk)
	form = ChoreForm(request.POST or None, instance=chore)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Chore updated.')
		return redirect('chores:index')
	return render(request, 'chores/chore_form.html', {'form': form, 'title': 'Edit chore'})


def chore_delete(request, pk):
	chore = get_object_or_404(Chore, pk=pk)
	if request.method == 'POST':
		chore.delete()
		messages.success(request, 'Chore removed.')
		return redirect('chores:index')
	return render(request, 'chores/confirm_delete.html', {
		'object': chore,
		'object_type': 'chore',
		'cancel_url': 'chores:index',
	})


@require_POST
def chore_complete(request, pk):
	chore = get_object_or_404(Chore, pk=pk)
	next_chore = chore.complete_and_create_next()
	if next_chore:
		messages.success(request, f'Chore completed. Next assignment: {next_chore.assignee.name}.')
	else:
		messages.success(request, 'Chore completed.')
	return redirect('chores:index')
