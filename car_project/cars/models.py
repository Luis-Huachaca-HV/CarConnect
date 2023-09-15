# cars/models.py
from django.utils import timezone
from django.db import models
from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.models import Sum

class CarConfig(AppConfig):
    name = 'cars'
    app_label = 'cars'
class Car(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    name = models.CharField(max_length=100,verbose_name="Nombre")
    model = models.CharField(max_length=100,verbose_name="Descripcion")
    year = models.PositiveIntegerField(verbose_name="Inicio")
    image = models.ImageField(null=True,verbose_name="Imagen", blank=True,upload_to="images/") 
    
    variable_type = models.CharField(max_length=10,verbose_name="Tipo de Variable", choices=[('millas', 'Millas'), ('kilometros', 'Kilómetros')])
    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"
    @property
    def Gasto_Total_en_Mantenimientos(self):
        return self.maintenances.aggregate(sum_total=models.Sum('total_spent'))['sum_total']

    @property
    def Seccion_Mas_Cara(self):
        tag_expenses = self.expenses.values('tag__name').annotate(total_amount=models.Sum('amount')).order_by('-total_amount')
        if tag_expenses:
            return tag_expenses[0]['tag__name']
        return None
    @property
    def Gasto_Promedio(self):
        first_maintenance = self.maintenances.earliest('date')
        last_maintenance = self.maintenances.latest('date')

        total_spending = Expense.objects.filter(maintenance__car=self).aggregate(sum_total=Sum('amount'))['sum_total']
        total_months = (last_maintenance.date - first_maintenance.date).days // 30

        if total_months > 0:
            average_spending = total_spending / total_months
            return average_spending
        else:
            return 0
    @property
    def Ultimo_Kilometraje_de_Mantenimiento(self):
        last_maintenance = self.maintenances.order_by('-date').first()
        if last_maintenance:
            return last_maintenance.mileage_km
        return None
    def __str__(self):
        return f"{self.name} {self.model} ({self.year})"
    
    
# models.py

class Document(models.Model):
    car = models.ForeignKey(Car,verbose_name="Carro", on_delete=models.CASCADE)
    title = models.CharField(max_length=100,verbose_name="Fecha")
    picture = models.ImageField(upload_to='documents/images/',verbose_name="Imagen")  # ImageField for images
    file = models.FileField(upload_to='documents/files/',verbose_name="Archivo")       # FileField for files
    due_date = models.DateField(verbose_name="Fecha de Mantenimiento")
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('upload_document', args=[str(self.car_id), str(self.id)])

# models.py
from django.urls import reverse

class Maintenance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE,verbose_name="Carro", related_name='maintenances')  # Added related_name
    date = models.DateField(verbose_name="Fecha")
    hour_meter = models.PositiveIntegerField(verbose_name="Horometro")
    mileage_km = models.PositiveIntegerField(verbose_name="Kilometraje")
    total_spent = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Total Gastado", default=0)
    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
    def __str__(self):
        return f"{self.id} , {self.car.name} , {self.date}"

    def get_absolute_url(self):
        return reverse('maintenance-update', args=[str(self.car_id), str(self.id)])

    

class ExpenseTag(models.Model):
    name = models.CharField(max_length=100,verbose_name="Nombre")
    class Meta:
        verbose_name = "Etiqueta de Gasto"
        verbose_name_plural = "Etiquetas de Gastos"
    def __str__(self):
        return f"{self.name} , {self.id}"


class Expense(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE,verbose_name="Carro", related_name='expenses')  # Added related_name
    maintenance = models.ForeignKey(Maintenance,verbose_name="Mantenimiento" ,on_delete=models.CASCADE)
    tag = models.ForeignKey(ExpenseTag,verbose_name="Etiqueta", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Fecha")
    amount = models.DecimalField(max_digits=10,verbose_name="cantidad", decimal_places=2, default=0)
    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
    def __str__(self):
        return f"{self.maintenance.id} , {self.tag}"

    def get_absolute_url(self):
        return reverse('maintenance-update', args=[str(self.car_id), str(self.maintenance.id)])


