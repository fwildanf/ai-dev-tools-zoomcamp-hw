from datetime import date, timedelta
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models


class HouseholdMember(models.Model):
	name = models.CharField(max_length=80, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class Chore(models.Model):
	ONE_TIME = 'one_time'
	DAILY = 'daily'
	WEEKLY = 'weekly'
	MONTHLY = 'monthly'
	FREQUENCY_CHOICES = [
		(ONE_TIME, 'One time'),
		(DAILY, 'Daily'),
		(WEEKLY, 'Weekly'),
		(MONTHLY, 'Monthly'),
	]

	name = models.CharField(max_length=120)
	assignee = models.ForeignKey(
		HouseholdMember,
		on_delete=models.CASCADE,
		related_name='chores',
	)
	due_date = models.DateField()
	frequency = models.CharField(
		max_length=10,
		choices=FREQUENCY_CHOICES,
		default=ONE_TIME,
	)
	completed = models.BooleanField(default=False)
	completed_at = models.DateTimeField(null=True, blank=True)
	recurrence_id = models.UUIDField(default=uuid4, editable=False)
	rotation_position = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['completed', 'due_date', 'name']

	def __str__(self):
		return self.name

	@property
	def is_overdue(self):
		return not self.completed and self.due_date < date.today()

	def clean(self):
		if not self.name.strip():
			raise ValidationError({'name': 'Chore name cannot be blank.'})
		if self.frequency not in dict(self.FREQUENCY_CHOICES):
			raise ValidationError({'frequency': 'Choose a valid frequency.'})

	def next_due_date(self):
		if self.frequency == self.DAILY:
			return self.due_date + timedelta(days=1)
		if self.frequency == self.WEEKLY:
			return self.due_date + timedelta(days=7)
		if self.frequency == self.MONTHLY:
			month = self.due_date.month % 12 + 1
			year = self.due_date.year + (self.due_date.month // 12)
			day = min(self.due_date.day, [31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
			return self.due_date.replace(year=year, month=month, day=day)
		return None

	def next_assignee(self):
		members = list(HouseholdMember.objects.order_by('pk'))
		if not members:
			return self.assignee
		try:
			current_index = [member.pk for member in members].index(self.assignee_id)
		except ValueError:
			current_index = -1
		return members[(current_index + 1) % len(members)]

	def complete_and_create_next(self):
		if self.completed:
			return None
		from django.utils import timezone

		self.completed = True
		self.completed_at = timezone.now()
		self.save(update_fields=['completed', 'completed_at', 'updated_at'])

		next_due_date = self.next_due_date()
		if next_due_date is None:
			return None
		return Chore.objects.create(
			name=self.name,
			assignee=self.next_assignee(),
			due_date=next_due_date,
			frequency=self.frequency,
			recurrence_id=self.recurrence_id,
			rotation_position=self.rotation_position + 1,
		)
