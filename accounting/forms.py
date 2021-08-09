from django import forms
from accounting.models import *


class ExpenseGroupForm(forms.ModelForm):
    class Meta:
        model = ExpenseGroup
        fields = ['avatar']
