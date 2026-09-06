from django import forms

from .models import Chore, HouseholdMember


PREDEFINED_CHORES = [
    ('Clean kitchen', 'Clean kitchen'),
    ('Do laundry', 'Do laundry'),
    ('Take out trash', 'Take out trash'),
    ('Vacuum floors', 'Vacuum floors'),
    ('Grocery shopping', 'Grocery shopping'),
]


class HouseholdMemberForm(forms.ModelForm):
    class Meta:
        model = HouseholdMember
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Member name'}),
        }


class ChoreForm(forms.ModelForm):
    name = forms.CharField(required=False)
    preset = forms.ChoiceField(
        required=False,
        choices=[('', 'Custom chore')] + PREDEFINED_CHORES,
    )

    class Meta:
        model = Chore
        fields = ['name', 'preset', 'assignee', 'due_date', 'frequency']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Chore name'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = (cleaned_data.get('name') or '').strip()
        preset = cleaned_data.get('preset')
        if preset and not name:
            cleaned_data['name'] = preset
        elif not name:
            self.add_error('name', 'Enter a chore name or choose a predefined chore.')
        return cleaned_data
