from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/<int:car_id>/documents/', views.documents_list, name='documents-list'),
    path('cars/<int:car_id>/document_upload/<int:document_id>', views.upload_document, name='upload_document'),
    path('cars/<int:car_id>/maintenance/', views.MaintenanceListView.as_view(), name='maintenance-list'),
    path('cars/<int:car_id>/maintenance/create/', views.maintenance_create, name='maintenance-create'),
    path('cars/<int:car_id>/maintenance/update/<int:maintenance_id>/', views.maintenance_detail, name='maintenance_detail'),
    path('cars/<int:car_id>/maintenance<int:maintenance_id>/new_tags/<int:expense_id>/', views.add_expense_tags, name='add-expense-tags'),

    #path('cars/<int:car_id>/documents/', views.car_documents, name='car_documents'),
]
