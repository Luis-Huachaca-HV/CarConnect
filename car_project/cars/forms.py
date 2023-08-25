from django import forms
from .models import Maintenance, ExpenseTag, Expense, Document
from django.forms import inlineformset_factory

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['date', 'hour_meter', 'mileage_km', 'total_spent']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'datepicker',  # Add a class for the datepicker
                'placeholder': 'YYYY-MM-DD',
            }),
        }
#ExpenseTagFormSet = inlineformset_factory(Maintenance, ExpenseTag, fields=['tag', 'amount'], extra=0)
from .models import ExpenseTag

class AddExpenseTagForm(forms.Form):
    expense_tags = forms.ModelMultipleChoiceField(
        queryset=ExpenseTag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['car', 'title', 'picture', 'due_date']
        
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['tag', 'date', 'amount']

