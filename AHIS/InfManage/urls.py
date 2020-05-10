from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.LogIn),
    path('LogIn.html',views.LogIn),
    path('PWChange.html',views.PWChange),
    
    path('Index.html',views.Index),
    
    path('StockInfQuery.html',views.StockInfQuery),
    path('StockInfAdd.html',views.StockInfAdd),
    path('StockInfEdit.html',views.StockInfEdit),
    path('StockInfDetail.html',views.StockInfDetail),
    path('StockInfVisualization.html',views.StockInfVisualization),

    path('DoctorInfQuery.html',views.DoctorInfQuery),
    path('DoctorInfAdd.html',views.DoctorInfAdd),
    path('DoctorInfEdit.html',views.DoctorInfEdit),
    path('DoctorInfDetail.html',views.DoctorInfDetail),
    path('DoctorInfVisualization.html',views.DoctorInfVisualization),

    path('DrugInfQuery.html',views.DrugInfQuery),
    path('DrugInfAdd.html',views.DrugInfAdd),
    path('DrugInfEdit.html',views.DrugInfEdit),
    path('DrugInfDetail.html',views.DrugInfDetail),
    path('DrugInfVisualization.html',views.DrugInfVisualization),

    path('CaseInfQuery.html',views.CaseInfQuery),
    path('CaseInfAdd.html',views.CaseInfAdd),
    path('CaseInfEdit.html',views.CaseInfEdit),
    path('CaseInfDetail.html',views.CaseInfDetail),
    path('CaseInfVisualization.html',views.CaseInfVisualization),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
