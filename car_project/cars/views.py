from datetime import date
from typing import Any, Dict
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import MaintenanceForm
from .models import Maintenance, ExpenseTag, Document
from .forms import DocumentForm

from django.forms import inlineformset_factory
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Maintenance, Expense
from .forms import MaintenanceForm, ExpenseForm
# views.py
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import Expense, ExpenseTag
from .forms import AddExpenseTagForm
# Create your views here.
# cars/views.py
from django.shortcuts import render, redirect
from .models import Car, Expense, ExpenseTag, Maintenance
from django.contrib.auth.decorators import login_required
from .tasks import send_document_reminder

@login_required
def send_reminder(request):
    user_email = request.user.email
    send_document_reminder.delay(user_email)
    # Add any response or redirection logic here

def maintenance_create(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.car = car
            maintenance.save()
            return redirect('maintenance_detail', car_id=car_id, maintenance_id=maintenance.id)
    else:
        form = MaintenanceForm()

    return render(request, 'forms/maintenance_create.html', {'car': car, 'form': form})

def documents_list(request,car_id):
    try:
        car = get_object_or_404(Car, id=car_id)
        documents = Document.objects.filter(car=car)
    except Car.DoesNotExist:
        # Handle if the car doesn't exist
        documents = []

    context = {
        'car': car,
        'documents': documents,
    }

    return render(request, 'documents/documents_list.html', context)

def upload_document(request, car_id,document_id):
    car = get_object_or_404(Car, id=car_id)
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('upload_document', car_id=car_id, document_id=document_id)
    else:
        form = DocumentForm(instance=document)
    
    context = {'form': form, 'car_id':car, 'document':document}
    return render(request, 'documents/document_form.html', context)




def maintenance_detail(request, car_id, maintenance_id):
    maintenance = get_object_or_404(Maintenance, car_id=car_id, id=maintenance_id)
    expenses = Expense.objects.filter(maintenance=maintenance)
    maintenance_form = MaintenanceForm(instance=maintenance)

    expense_forms = []
    for expense in expenses:
        if request.method == 'POST' and f'update_expense_{expense.id}' in request.POST:
            expense_form = ExpenseForm(request.POST, instance=expense)
            if expense_form.is_valid():
                expense_form.save()
                return redirect('maintenance_detail', car_id=expense.car_id, maintenance_id=maintenance_id)

        else:
            expense_form = ExpenseForm(instance=expense)
        expense_form.expense_id = expense.id
        expense_forms.append(expense_form)

    return render(request, 'forms/maintenance_update.html', {
        'car_id': car_id,
        'maintenance_id': maintenance_id,
        'maintenance': maintenance,
        'expenses': expenses,
        'maintenance_form': maintenance_form,
        'expense_forms': expense_forms,
    })

def add_expense_tags(request, car_id, maintenance_id, expense_id):
    expense = None

    if expense_id != 0:
        expense = get_object_or_404(Expense, pk=expense_id)

    if request.method == 'POST':
        form = AddExpenseTagForm(request.POST)
        if form.is_valid():
            selected_tags = form.cleaned_data['expense_tags']
            for tag in selected_tags:
                if expense_id == 0:  # For initialization
                    # Create an initial expense record for the selected tag
                    expense = Expense.objects.create(
                        car=Car.objects.get(pk=car_id),
                        maintenance=Maintenance.objects.get(pk=maintenance_id),
                        tag=tag,
                        date=date.today(),
                        amount=0  # Initialize with zero amount
                    )
                else:
                    # Update the existing expense record with the selected tag
                    expense.tag = tag
                    expense.save()

            return redirect('maintenance_detail', car_id=car_id, maintenance_id=maintenance_id)
    else:
        unlinked_tags = ExpenseTag.objects.exclude(expense__maintenance__id=maintenance_id)
        form = AddExpenseTagForm()

    return render(request, 'forms/add_expense_tags.html', {'form': form, 'unlinked_tags': unlinked_tags})



class MaintenanceDeleteView(DeleteView):
    model = Maintenance
    success_url = reverse_lazy('maintenance-list')


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'home/car_detail.html', {'car': car})


@login_required
def car_list(request):
    cars = Car.objects.filter(user=request.user)
    return render(request, 'home/list_car.html', {'cars': cars})



#quitar esto y poner un def con lo que necesitamos
class MaintenanceListView(ListView):
    model = Maintenance
    template_name = 'maintenance_list.html'
    context_object_name = 'maintenance_list'

  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = self.kwargs.get('car_id')

        context['car'] = get_object_or_404(Car, id=car_id)

        context['maintenance_list_id'] = Maintenance.objects.filter(car_id=car_id)

        
        return context

    


def home_view(request):
    #if request.method == 'POST':
    return render(request, 'home/home_view.html')