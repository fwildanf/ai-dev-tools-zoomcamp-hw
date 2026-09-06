from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Chore, HouseholdMember


class ChoreModelTests(TestCase):
	def setUp(self):
		self.alex = HouseholdMember.objects.create(name='Alex')
		self.jordan = HouseholdMember.objects.create(name='Jordan')

	def test_blank_chore_name_is_invalid(self):
		chore = Chore(
			name='   ',
			assignee=self.alex,
			due_date=date.today(),
		)
		with self.assertRaises(ValidationError):
			chore.full_clean()

	def test_recurring_due_dates_advance_by_frequency(self):
		start = date(2026, 1, 31)
		expected_dates = {
			Chore.DAILY: date(2026, 2, 1),
			Chore.WEEKLY: date(2026, 2, 7),
			Chore.MONTHLY: date(2026, 2, 28),
		}
		for frequency, expected in expected_dates.items():
			chore = Chore(
				name='Sweep',
				assignee=self.alex,
				due_date=start,
				frequency=frequency,
			)
			self.assertEqual(chore.next_due_date(), expected)

	def test_completing_recurring_chore_preserves_history_and_rotates_assignee(self):
		chore = Chore.objects.create(
			name='Take out trash',
			assignee=self.alex,
			due_date=date.today(),
			frequency=Chore.WEEKLY,
		)

		next_chore = chore.complete_and_create_next()

		chore.refresh_from_db()
		self.assertTrue(chore.completed)
		self.assertIsNotNone(chore.completed_at)
		self.assertEqual(next_chore.assignee, self.jordan)
		self.assertEqual(next_chore.due_date, date.today() + timedelta(days=7))
		self.assertEqual(next_chore.recurrence_id, chore.recurrence_id)

	def test_completing_one_time_chore_does_not_create_next_occurrence(self):
		chore = Chore.objects.create(
			name='Buy milk',
			assignee=self.alex,
			due_date=date.today(),
		)

		self.assertIsNone(chore.complete_and_create_next())
		self.assertEqual(Chore.objects.count(), 1)

	def test_incomplete_past_chore_is_overdue(self):
		chore = Chore.objects.create(
			name='Clean kitchen',
			assignee=self.alex,
			due_date=date.today() - timedelta(days=1),
		)
		self.assertTrue(chore.is_overdue)
		chore.completed = True
		self.assertFalse(chore.is_overdue)


class ChoreViewTests(TestCase):
	def setUp(self):
		self.alex = HouseholdMember.objects.create(name='Alex')
		self.jordan = HouseholdMember.objects.create(name='Jordan')
		self.chore = Chore.objects.create(
			name='Clean kitchen',
			assignee=self.alex,
			due_date=date.today(),
		)

	def test_dashboard_shows_workload_and_overdue_status(self):
		overdue = Chore.objects.create(
			name='Overdue task',
			assignee=self.jordan,
			due_date=date.today() - timedelta(days=1),
		)

		response = self.client.get(reverse('chores:index'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Alex')
		self.assertContains(response, 'Clean kitchen')
		self.assertContains(response, 'Overdue task')
		self.assertContains(response, 'Overdue')
		self.assertContains(response, str(overdue.pk))

	def test_dashboard_filters_by_assignee(self):
		Chore.objects.create(
			name='Jordan task',
			assignee=self.jordan,
			due_date=date.today(),
		)

		response = self.client.get(reverse('chores:index'), {'assignee': self.alex.pk})

		self.assertContains(response, 'Clean kitchen')
		self.assertEqual([chore.name for chore in response.context['chores']], ['Clean kitchen'])

	def test_member_crud(self):
		response = self.client.post(reverse('chores:member_create'), {'name': 'Sam'})
		self.assertRedirects(response, reverse('chores:index'))
		sam = HouseholdMember.objects.get(name='Sam')

		response = self.client.post(reverse('chores:member_edit', args=[sam.pk]), {'name': 'Samantha'})
		self.assertRedirects(response, reverse('chores:index'))
		self.assertTrue(HouseholdMember.objects.filter(name='Samantha').exists())

		response = self.client.post(reverse('chores:member_delete', args=[sam.pk]))
		self.assertRedirects(response, reverse('chores:index'))
		self.assertFalse(HouseholdMember.objects.filter(pk=sam.pk).exists())

	def test_chore_create_supports_predefined_chore(self):
		response = self.client.post(reverse('chores:chore_create'), {
			'name': '',
			'preset': 'Do laundry',
			'assignee': self.jordan.pk,
			'due_date': date.today().isoformat(),
			'frequency': Chore.WEEKLY,
		})

		self.assertRedirects(response, reverse('chores:index'))
		chore = Chore.objects.get(name='Do laundry')
		self.assertEqual(chore.assignee, self.jordan)

	def test_chore_crud_and_completion(self):
		response = self.client.post(reverse('chores:chore_edit', args=[self.chore.pk]), {
			'name': 'Clean the kitchen',
			'preset': '',
			'assignee': self.jordan.pk,
			'due_date': date.today().isoformat(),
			'frequency': Chore.WEEKLY,
		})
		self.assertRedirects(response, reverse('chores:index'))
		self.chore.refresh_from_db()
		self.assertEqual(self.chore.name, 'Clean the kitchen')
		self.assertEqual(self.chore.assignee, self.jordan)

		response = self.client.post(reverse('chores:chore_complete', args=[self.chore.pk]))
		self.assertRedirects(response, reverse('chores:index'))
		self.chore.refresh_from_db()
		self.assertTrue(self.chore.completed)
		self.assertEqual(Chore.objects.filter(recurrence_id=self.chore.recurrence_id).count(), 2)

		next_chore = Chore.objects.exclude(pk=self.chore.pk).get(recurrence_id=self.chore.recurrence_id)
		response = self.client.post(reverse('chores:chore_delete', args=[next_chore.pk]))
		self.assertRedirects(response, reverse('chores:index'))
		self.assertFalse(Chore.objects.filter(pk=next_chore.pk).exists())

	def test_completion_requires_post(self):
		response = self.client.get(reverse('chores:chore_complete', args=[self.chore.pk]))
		self.assertEqual(response.status_code, 405)
