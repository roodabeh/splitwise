from django import forms


class ExpenseGroupForm(forms.Form):
    name = forms.CharField()
    avatar = forms.ImageField()
