from django.contrib import admin
from InfManage.models import DoctorInf,DrugInf,ManagerInf,StockInInf,CaseInf
# Register your models here.

admin.site.register(DoctorInf)
admin.site.register(DrugInf)
admin.site.register(StockInInf)
admin.site.register(ManagerInf)
admin.site.register(CaseInf)