from django.db import models
from django.utils import timezone

# Create your models here.
# 医生信息表
class DoctorInf(models.Model):
    # 医生编号
    DoctorID = models.CharField(max_length=9,primary_key=True,unique=True,blank=False,null=False)
    # 姓名
    Name = models.CharField(max_length=30,blank=False)
    # 性别
    Sex = models.CharField(max_length=2,blank=False)
    # 年龄
    Age = models.IntegerField(blank=False)
    # 照片
    Photo = models.ImageField(default="None",blank=False)
    # 联系方式
    Tel = models.CharField(max_length=11,blank=False)
    # 职务
    Position = models.CharField(max_length=20,blank=False)
    # 科室
    Office = models.CharField(max_length=20,blank=False)
    # 科室位置
    OfficeSite = models.CharField(max_length=20,blank=False)
    # 工作时间
    WorkTime = models.CharField(max_length=11,blank=False)
    # 学历
    Education = models.CharField(max_length=20,default="None")
    # 介绍
    Introduce = models.TextField(default="None",blank=False)
    # 主要成果
    Achievements = models.TextField(default="None",blank=False)
    # 特长
    Characters = models.TextField(default="None",blank=False)
    # 类别
    Category = models.CharField(max_length=10,blank=False)

# 药品进货表
class StockInInf(models.Model):
    # 入库单号
    StockInID = models.CharField(max_length=12,primary_key=True,unique=True,blank=False,null=False)
    # 入库方式
    StockInType = models.CharField(max_length=8,blank=False)
    # 入库日期
    StockInDate = models.DateField(default=timezone.now)
    # 供货单位
    DeliveryUnit = models.CharField(max_length=20,blank=False)
    # 发票号
    InvoiceID = models.CharField(max_length=12,blank=False)
    # 发票日期
    InvoiceDate = models.DateField(default=timezone.now)
    # 药物编号
    DrugID = models.CharField(max_length=5,blank=False)
    # 药物名称
    DrugName = models.CharField(max_length=20,blank=False)
    # 产地
    Origin = models.CharField(max_length=20,blank=False)
    # 批发价
    WholesalePrice = models.FloatField(blank=False)
    # 零售价
    RetailPrice = models.FloatField(blank=False)
    # 药品进价
    DrugPurPrice = models.FloatField(blank=False)
    # 药品数量
    DrugNum = models.IntegerField(blank=False)
    # 进价金额
    PurchaseSum = models.FloatField(blank=False)
    # 有效期
    EffectiveTime = models.IntegerField(blank=False)
    # 生产日期
    ProduceDate = models.DateField()
    # 备注
    Remark = models.TextField(default='None')
 

# 药品库存表
class DrugInf(models.Model):
    # 药品编号
    DrugID = models.CharField(primary_key=True,max_length=5,blank=False,null=False)
    # 药品名称
    DrugName = models.CharField(max_length=20,blank=False)
    # 供货单位
    DeliveryUnit = models.CharField(max_length=20,blank=False)
    # 生产日期
    ProduceDate = models.DateField(default = timezone.now)
    # 有效期
    EffectiveTime = models.IntegerField(blank=False)
    # 零售价
    RetailPrice = models.FloatField(blank=False)
    # 批发价
    WholesalePrice = models.FloatField(blank=False)
    # 药品进价
    DrugPurPrice = models.FloatField(blank=False)
    # 药品数量
    DrugNum = models.IntegerField(blank=False)
    # 成分
    Component = models.TextField(default="none")
    # 性状
    Character = models.TextField(default="none")
    # 适应症
    Indication = models.TextField(default="none")
    # 规格
    Specs = models.TextField(default="none")
    # 用法
    Usage = models.TextField(default="none")
    # 不良反应
    SideEffect = models.TextField(default="none")
    # 禁忌
    Taboo = models.TextField(default="none")
    # 注意事项
    Note = models.TextField(default="none")
    # 孕妇及哺乳期妇女用药
    Gravida = models.TextField(default="none")
    # 儿童用药
    ChildDrug = models.TextField(default="none")
    # 老年人用药
    OlderDrug = models.TextField(default="none")
    # 药物相互作用
    DrugInteraction = models.TextField(default="none")
    # 药物过量
    DrugOverdose = models.TextField(default="none")
    # 药物毒理
    DrugToxicology = models.TextField(default="none")
    # 贮藏
    Store = models.TextField(default="none")
    # 包装
    Packing = models.TextField(default="none")
    # 执行标准
    ExecutiveStard = models.TextField(default="none")
    # 标注位
    Flag = models.CharField(max_length=1,blank=False)

# 管理人员信息表
class ManagerInf(models.Model):
    # 管理员编号
    ManagerID = models.CharField(max_length=9,primary_key=True,unique=True,null=False)
    # 登录密码
    PassWord = models.CharField(max_length=20,blank=False,null=False)
    # 管理员姓名
    ManagerName = models.CharField(max_length=20,blank=False,null=False)
    # 管理员性别
    ManagerSex = models.CharField(max_length=2,blank=False)
    # 联系方式
    Tel = models.CharField(max_length=11,blank=False,unique=False)
    # 电子邮件
    Email = models.EmailField(unique=True)

# 病例信息
class CaseInf(models.Model):
    # 病例编号
    CaseID = models.CharField(max_length=12,primary_key=True,unique=True,blank=False,null=False)
    # 宠物主姓名
    PetOwnerName = models.CharField(max_length=20,blank=False,null=False)
    # 宠物主性别
    PetOwnerSex = models.CharField(max_length=2,blank=False,null=False)
    # 联系方式
    Tel = models.CharField(max_length=11,blank=False,null=False)
    # 电子邮件
    Email = models.EmailField(unique=True)
    # 邮政编码
    PostCode = models.CharField(max_length=6,blank=False)
    # 家庭住址
    Address = models.CharField(max_length=30,blank=False,null=False)
    # 宠物姓名
    PetName = models.CharField(max_length=20,blank=False)
    # 品种
    Breed = models.CharField(max_length=20,blank=False)
    # 宠物性别
    PetSex = models.CharField(max_length=2,blank=False)
    # 宠物年龄
    PetAge = models.IntegerField(blank=False)
    # 宠物体重
    PetWeight = models.FloatField(blank=False)
    # 免疫情况
    Immune = models.CharField(max_length=30,blank=False)
    # 绝育情况
    Sterilization = models.CharField(max_length=30,blank=False)
    # 宠物证编号
    PetCardID = models.CharField(max_length=12,blank=False,null=False)
    # 医生编号
    DoctorID = models.CharField(max_length=9,blank=False,null=False)
    # 诊断信息
    Treatment = models.TextField(default="none")
    # 处方信息
    Prescription = models.TextField(default="none")
    # 总金额
    TotalSum = models.FloatField(blank=False)
