from django.contrib import admin

# Register your models here.
# cars/admin.py
from django.contrib import admin
from .models import Car, Expense, ExpenseTag, Document, Maintenance
from django.contrib import admin
from .models import Car

class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'year', 'Gasto_Total_en_Mantenimientos', 'Seccion_Mas_Cara', 'Gasto_Promedio', 'Ultimo_Kilometraje_de_Mantenimiento']

admin.site.register(Car, CarAdmin)

admin.site.register(Expense)
admin.site.register(ExpenseTag)
admin.site.register(Document)
admin.site.register(Maintenance)
