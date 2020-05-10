from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from InfManage import models
from InfManage.form import UserForm
from django.contrib import messages
from InfManage.function import is_have_alpha
from django.db.models import Sum

# Create your views here.

"""登录"""
def LogIn(request):
    register_form = UserForm(request.POST)
    # 清除存储持久化session信息
    if 'id' in request.session.keys():
        del request.session['id']
    if request.method =="POST":
        ManagerID = request.POST.get('ManagerID',None)
        PassWord = request.POST.get('PassWord',None)
        try:
            # 判断帐号、密码
            if not models.ManagerInf.objects.filter(ManagerID = ManagerID,PassWord = PassWord):
                messages.error(request,'帐号或密码错误，请重新输入。')
                return render(request,'LogIn.html',{'register_form':register_form})
            # 判断验证码
            elif not register_form.is_valid():
                messages.error(request,'验证码错误，请重新输入。')
                return render(request,'LogIn.html',{'register_form':register_form})
            else:
                # 将编号存储到session中用于持久化
                request.session['id'] = ManagerID
                return render(request,'Index.html')
        except:
            return render(request,'LogIn.html',{'register_form':register_form})
    return render(request,'LogIn.html',{'register_form':register_form})


# 密码修改
def PWChange(request):
    if request.method == "POST":
        ManagerID = request.POST.get("ManagerID",None)
        PassWord = request.POST.get("PassWord",None)
        NewPassWord1 = request.POST.get("NewPassWord1",None)
        NewPassWord2 = request.POST.get("NewPassWord2",None)
        try:
            tmp = models.ManagerInf.objects.filter(ManagerID = ManagerID,PassWord = PassWord)
            # 判断帐号是否存在以及密码是否正确
            if len(tmp) == 0:
                messages.error(request,"该账号不存在或密码错误。")
            else:
                # 判断新密码是否一致
                if NewPassWord1 != NewPassWord2:
                    messages.error(request,"两次输入密码不一致，请检查后重新输入。")
                elif NewPassWord1 == tmp[0].PassWord:
                    messages.error(request,"新密码与原密码一致，请检查后重新输入。")
                else:
                    tmp[0].PassWord = NewPassWord1
                    tmp[0].save()
                    messages.error(request,"密码修改成功。")
                    return render(request,'LogIn.html')
        except:
            pass
    return render(request,'PWChange.html')


"""基页面"""
def Index(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        return render(request,'Index.html')
    # id存在，但值未在数据库中


"""库存信息查询"""
def StockInfQuery(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            SearchWd =  request.POST.get('SearchWd',None)
            try:
                if SearchWd =="":
                    tmp = models.StockInInf.objects.all().order_by("StockInID")
                    return render(request,'StockInfQuery.html',{'SearchInf':tmp})
                # 按入库单号查询
                elif SearchWd[0] == "S" and SearchWd[1:].isdigit():
                    tmp = models.StockInInf.objects.filter(StockInID = SearchWd).order_by("StockInID")
                    return render(request,'StockInfQuery.html',{'SearchInf':tmp})
                # 按药物编号查询
                elif SearchWd.isdigit():
                    tmp = models.StockInInf.objects.filter(DrugID = SearchWd).order_by("StockInID")
                    return render(request,'StockInfQuery.html',{'SearchInf':tmp})
                # 按药物名称查询
                else:
                    tmp = models.StockInInf.objects.filter(DrugName = SearchWd).order_by("StockInID")
                    return render(request,'StockInfQuery.html',{'SearchInf':tmp})
            except:
                return render(request,'StockInfQuery.html')
        elif request.method == "GET":
            method = request.GET.get("method")
            StockInID = request.GET.get("id")
            # 1表示删除
            if method == "1":
                tmp1 = models.StockInInf.objects.get(StockInID = StockInID)
                tmp2 = models.DrugInf.objects.get(DrugID = tmp1.DrugID)
                # 判断库存量是否大于订单数量
                if tmp2.DrugNum < tmp1.DrugNum:
                    messages.error(request,'该药品库存量小于该订单数量，删除失败。')
                else:
                    tmp2.DrugNum = tmp2.DrugNum - tmp1.DrugNum
                    tmp2.save()
                    models.StockInInf.objects.filter(StockInID = StockInID).delete()
                    messages.error(request,"删除成功。")
                tmp = models.StockInInf.objects.all().order_by("StockInID")
                return render(request,'StockInfQuery.html',{'SearchInf':tmp})
            # 2表示编辑
            elif method == "2":
                tmp = models.StockInInf.objects.filter(StockInID = StockInID)
                return render(request,'StockInfEdit.html',{'SearchInf':tmp})
        return render(request,'StockInfQuery.html')


"""库存信息添加"""
def StockInfAdd(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            StockInType = request.POST.get("StockInType",None)
            DeliveryUnit = request.POST.get("DeliveryUnit",None)
            StockInDate  = request.POST.get("StockInDate",None)
            StockInID = request.POST.get("StockInID",None)#长度11开头S
            InvoiceID = request.POST.get("InvoiceID",None)#长度11开头I
            InvoiceDate = request.POST.get("InvoiceDate",None)
            DrugID = request.POST.get("DrugID",None)#长度5
            DrugName = request.POST.get("DrugName",None)
            Origin = request.POST.get("Origin",None)
            ProduceDate = request.POST.get("ProduceDate",None)
            EffectiveTime = int(request.POST.get("EffectiveTime",None))#>0
            RetailPrice = float(request.POST.get("RetailPrice",None))#>0
            WholesalePrice = float(request.POST.get("WholesalePrice",None))#>0
            DrugPurPrice = float(request.POST.get("DrugPurPrice",None))#>0
            DrugNum = int(request.POST.get("DrugNum",None))#>0
            PurchaseSum = float(request.POST.get("PurchaseSum",None))#>0
            Remark = request.POST.get("Remark",None)
            try:
                # 判断入库单号是否存在
                if models.StockInInf.objects.filter(StockInID = StockInID):
                    messages.error(request,'入库单号重复，请重新输入。')
                    return render(request,'StockInfAdd.html')
                # 判断发票单号是否存在 
                elif models.StockInInf.objects.filter(InvoiceID = InvoiceID):
                    messages.error(request,'发票单号重复，请重新输入。')
                    return render(request,'StockInfAdd.html')
                # 判断入库单号、发票单号是否符合规范
                elif (StockInID[0] != "S" or InvoiceID[0] != "I") or (len(StockInID) != 12 or len(InvoiceID) != 12):
                    messages.error(request,'入库单号或发票单号不符合规范，请重新输入。')
                    return render(request,'StockInfAdd.html')
                # 判断药品编号是否符合规范
                elif len(DrugID) != 5:
                    messages.error(request,'药品编号不符合规范，请重新输入')
                    return render(request,'StockInfAdd.html')
                # 判断有效期是否符合实际
                elif EffectiveTime <= 0:
                    messages.error(request,"有效期应＞0，请重新输入。")
                    return render(request,'StockInfAdd.html')
                # 判断零售价是否符合实际
                elif RetailPrice <= 0:
                    messages.error(request,"零售价应＞0，请重新输入。")
                    return render(request,'StockInfAdd.html')
                # 判断批发价是否符合实际
                elif WholesalePrice <= 0:
                    messages.error(request,"批发价应＞0，请重新输入。")
                    return render(request,'StockInfAdd.html')
                # 判断药品进价是否符合实际
                elif DrugPurPrice <= 0:
                    messages.error(request,"药品进价应＞0，请重新输入。")
                    return render(request,'StockInfAdd.html')
                # 判断药品数量是否符合实际
                elif DrugNum <= 0:
                    messages.error(request,"药品数量应＞0，请重新输入。")
                    return render(request,'StockInfAdd.html')
                # 判断总金额是否符合实际
                elif PurchaseSum <= 0:
                    messages.error(request,"总金额应＞0，请重新输入。")
                    return render(request,'StockInfAdd.html')
                # 判断药品进价*药品数量是否等于总金额
                elif PurchaseSum != DrugNum * DrugPurPrice:
                    messages.error(request,"药品进价*药品数量应等于总金额，请重新输入。")
                    return render(request,'StockInfAdd.html')
                else:
                    # 进货单据入库
                    stock_in_add = models.StockInInf()
                    stock_in_add.StockInType = StockInType
                    stock_in_add.DeliveryUnit = DeliveryUnit
                    stock_in_add.StockInDate = StockInDate
                    stock_in_add.StockInID = StockInID
                    stock_in_add.InvoiceID = InvoiceID
                    stock_in_add.InvoiceDate = InvoiceDate
                    stock_in_add.DrugID = DrugID
                    stock_in_add.DrugName = DrugName
                    stock_in_add.Origin = Origin
                    stock_in_add.ProduceDate = ProduceDate
                    stock_in_add.EffectiveTime = EffectiveTime
                    stock_in_add.RetailPrice = RetailPrice
                    stock_in_add.WholesalePrice = WholesalePrice
                    stock_in_add.DrugPurPrice = DrugPurPrice
                    stock_in_add.DrugNum = DrugNum
                    stock_in_add.PurchaseSum =PurchaseSum
                    stock_in_add.Remark = Remark
                    stock_in_add.save()
                    # 药品已存在 更新有效期、零售价、批发价、药物进价、药品数量
                    if models.DrugInf.objects.filter(DrugID = DrugID):
                        tmp = models.DrugInf.objects.get(DrugID = DrugID)
                        tmp.EffectiveTime = EffectiveTime
                        tmp.RetailPrice = RetailPrice
                        tmp.WholesalePrice = WholesalePrice
                        tmp.DrugPurPrice = DrugPurPrice
                        tmp.DrugNum  = tmp.DrugNum + DrugNum
                        tmp.save()
                    # 药品不存在 药物表添加数据
                    else:
                        drug_add = models.DrugInf()
                        drug_add.DrugID = DrugID
                        drug_add.DrugName = DrugName
                        drug_add.DeliveryUnit = DeliveryUnit
                        drug_add.ProduceDate = ProduceDate
                        drug_add.EffectiveTime = EffectiveTime
                        drug_add.RetailPrice =  RetailPrice
                        drug_add.WholesalePrice = WholesalePrice
                        drug_add.DrugPurPrice = DrugPurPrice
                        drug_add.DrugNum = DrugNum
                        # 标记药品信息是否填写完全
                        drug_add.Flag = "0"
                        drug_add.save()

                    tmp = models.StockInInf.objects.all().order_by("StockInID")
                    return render(request,'StockInfAdd.html',{'SearchInf':tmp})
            except:
                return render(request,'StockInfAdd.html')
        return render(request,'StockInfAdd.html')


"""库存信息编辑"""
def StockInfEdit(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            StockInType = request.POST.get("StockInType",None)
            DeliveryUnit = request.POST.get("DeliveryUnit",None)
            StockInDate  = request.POST.get("StockInDate",None)
            StockInID = request.POST.get("StockInID",None)#长度11开头S
            InvoiceID = request.POST.get("InvoiceID",None)#长度11开头I
            InvoiceDate = request.POST.get("InvoiceDate",None)
            DrugID = request.POST.get("DrugID",None)#长度5
            DrugName = request.POST.get("DrugName",None)
            Origin = request.POST.get("Origin",None)
            ProduceDate = request.POST.get("ProduceDate",None)
            EffectiveTime = int(request.POST.get("EffectiveTime",None))#>0
            RetailPrice = float(request.POST.get("RetailPrice",None))#>0
            WholesalePrice = float(request.POST.get("WholesalePrice",None))#>0
            DrugPurPrice = float(request.POST.get("DrugPurPrice",None))#>0
            DrugNum = int(request.POST.get("DrugNum",None))#>0
            PurchaseSum = float(request.POST.get("PurchaseSum",None))#>0
            Remark = request.POST.get("Remark",None)
            try:
                # 判断入库单号、发票单号是否符合规范
                if (StockInID[0] != "S" or InvoiceID[0] != "I") or (len(StockInID) != 12 or len(InvoiceID) != 12):
                    messages.error(request,'入库单号或发票单号不符合规范，请重新输入。')
                    return render(request,'StockInfEdit.html')
                # 判断药品编号是否符合规范
                elif len(DrugID) != 5:
                    messages.error(request,'药品编号不符合规范，请重新输入')
                    return render(request,'StockInfEdit.html')
                # 判断有效期是否符合实际
                elif EffectiveTime <= 0:
                    messages.error(request,"有效期应＞0，请重新输入。")
                    return render(request,'StockInfEdit.html')
                # 判断零售价是否符合实际
                elif RetailPrice <= 0:
                    messages.error(request,"零售价应＞0，请重新输入。")
                    return render(request,'StockInfEdit.html')
                # 判断批发价是否符合实际
                elif WholesalePrice <= 0:
                    messages.error(request,"批发价应＞0，请重新输入。")
                    return render(request,'StockInfEdit.html')
                # 判断药品进价是否符合实际
                elif DrugPurPrice <= 0:
                    messages.error(request,"药品进价应＞0，请重新输入。")
                    return render(request,'StockInfEdit.html')
                # 判断药品数量是否符合实际
                elif DrugNum <= 0:
                    messages.error(request,"药品数量应＞0，请重新输入。")
                    return render(request,'StockInfEdit.html')
                # 判断总金额是否符合实际
                elif PurchaseSum <= 0:
                    messages.error(request,"总金额应＞0，请重新输入。")
                    return render(request,'StockInfEdit.html')
                # 判断药品进价*药品数量是否等于总金额
                elif PurchaseSum != DrugNum * DrugPurPrice:
                    messages.error(request,"药品进价*药品数量应等于总金额，请重新输入。")
                    return render(request,'StockInfEdit.html')
                else:
                    tmp = models.StockInInf.objects.get(StockInID = StockInID)
                    tmp.StockInType = StockInType
                    tmp.DeliveryUnit = DeliveryUnit
                    tmp.StockInDate = StockInDate
                    tmp.StockInID = StockInID
                    tmp.InvoiceID = InvoiceID
                    tmp.InvoiceDate = InvoiceDate
                    tmp.DrugID = DrugID
                    tmp.DrugName = DrugName
                    tmp.Origin = Origin
                    tmp.ProduceDate = ProduceDate
                    tmp.EffectiveTime = EffectiveTime
                    tmp.RetailPrice = RetailPrice
                    tmp.WholesalePrice = WholesalePrice
                    tmp.DrugPurPrice = DrugPurPrice
                    tmp.DrugNum = DrugNum
                    tmp.PurchaseSum =PurchaseSum
                    tmp.Remark = Remark
                    tmp.save()
                    messages.error(request,'修改成功。')
                    return render(request,'StockInfQuery.html')
            except:
                return render(request,'StockInfQuery.html')   
        return render(request,'StockInfEdit.html')


"""库存信息详细"""
def StockInfDetail(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "GET":
            StockInID = request.GET.get("id")
            tmp = models.StockInInf.objects.filter(StockInID = StockInID)
            return render(request,'StockInfDetail.html',{'SearchInf':tmp})


"""库存信息可视化"""
def StockInfVisualization(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            starttime = request.POST.get('starttime',None)
            endtime = request.POST.get('endtime',None)
            try:
                tmp = models.StockInInf.objects.filter(StockInDate__range = [starttime,endtime])
                if len(tmp) == 0:
                    messages.error(request,'该时间段内无进货信息。')
                    return render(request,'StockInfVisualization.html')
                else:
                    # 区间内日期
                    date = []
                    # 日期以及该日进货总开销
                    date_sum = {}
                    # 数据返回网页
                    data_back = []
                    for i in tmp:
                        date.append(i.StockInDate)
                    # 日期去重
                    date = list(set(date))
                    for i in date:
                        date_sum.update({i:0})
                    for i in date_sum.keys():
                        tmp1 = models.StockInInf.objects.filter(StockInDate = i).aggregate(sums = Sum("PurchaseSum"))
                        date_sum[i] = tmp1["sums"]
                    for i in date_sum.keys():
                        data_back.append({'name':str(i),'y':date_sum[i]})
                    
                    return render(request,'StockInfVisualization.html',{'data_back':data_back})
            except:
                return render(request,'StockInfVisualization.html')
        return render(request,'StockInfVisualization.html')


"""医生信息查询"""
def DoctorInfQuery(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            SearchWd =  request.POST.get('SearchWd',None)
            try:
                if SearchWd == "":
                    tmp = models.DoctorInf.objects.all().order_by("DoctorID")
                    return render(request,'DoctorInfQuery.html',{'SearchInf':tmp})
                # 查询医生编号
                elif len(SearchWd) == 9 and SearchWd.isdigit():
                    tmp = models.DoctorInf.objects.filter(DoctorID = SearchWd).order_by("DoctorID")
                    return render(request,'DoctorInfQuery.html',{'SearchInf':tmp})
                # 查询性别
                elif SearchWd == "男" or SearchWd == "女":
                    tmp = models.DoctorInf.objects.filter(Sex = SearchWd).order_by("DoctorID")
                    return render(request,'DoctorInfQuery.html',{'SearchInf':tmp}) 
                # 查询科室
                elif SearchWd[-1] == "科":
                    tmp = models.DoctorInf.objects.filter(Office = SearchWd).order_by("DoctorID")
                    return render(request,'DoctorInfQuery.html',{'SearchInf':tmp}) 
                # 查询姓名
                else:
                    tmp = models.DoctorInf.objects.filter(Name = SearchWd).order_by("DoctorID")
                    return render(request,'DoctorInfQuery.html',{'SearchInf':tmp}) 
            except:
                return render(request,'DoctorInfQuery.html')
        elif request.method == "GET":
            method = request.GET.get("method")
            DoctorID = request.GET.get("id")
            # 1表示删除
            if method == "1":
                models.DoctorInf.objects.filter(DoctorID = DoctorID).delete()
                tmp = models.DoctorInf.objects.all().order_by("DoctorID")
                messages.error(request,'删除成功。')
                return render(request,'DoctorInfQuery.html',{'SearchInf':tmp}) 
            # 2表示编辑
            elif method == "2":
                tmp = models.DoctorInf.objects.filter(DoctorID = DoctorID)
                return render(request,'DoctorInfEdit.html',{'SearchInf':tmp})
        return render(request,'DoctorInfQuery.html')


"""医生信息添加"""
def DoctorInfAdd(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method  == "POST":
            DoctorID = request.POST.get("DoctorID",None)
            Name = request.POST.get("Name",None)
            Sex = request.POST.get("Sex",None)
            Age = int(request.POST.get("Age",None))
            Photo = request.POST.get("Photo",None)
            Tel = request.POST.get("Tel",None)
            Position = request.POST.get("Position",None)
            Office = request.POST.get("Office",None)
            OfficeSite = request.POST.get("OfficeSite",None)
            WorkTime = request.POST.get("WorkTime",None)
            Education = request.POST.get("Education",None)
            Introduce = request.POST.get("Introduce",None)
            Achievements = request.POST.get("Achievements",None)
            Characters = request.POST.get("Characters",None)
            try:
                # 判断医生编号是否存在
                if models.DoctorInf.objects.filter(DoctorID = DoctorID):
                    messages.error(request,'医生帐号重复，请重新输入。')
                    return render(request,'DoctorInfAdd.html')
                # 判断医生编号是否合法
                elif len(DoctorID) != 9 or not DoctorID.isdigit():
                    messages.error(request,'医生编号不符合规范，请重新输入。')
                    return render(request,'DoctorInfAdd.html')
                # 判断年龄是否合法
                elif Age < 0:
                    messages.error(request,'年龄应＞0，请重新输入')
                    return render(request,'DoctorInfAdd.html')
                # 判断电话是否合法
                elif len(Tel) != 11 and is_have_alpha(Tel):
                    messages.error(request,'电话号码不符合规范，请从新输入。')
                    return render(request,'DoctorInfAdd.html')
                else:
                    doctor_add = models.DoctorInf()
                    doctor_add.DoctorID = DoctorID
                    doctor_add.Name = Name
                    doctor_add.Sex = Sex
                    doctor_add.Age = Age
                    doctor_add.Photo = Photo
                    doctor_add.Tel = Tel
                    doctor_add.Position = Position
                    doctor_add.Office = Office
                    doctor_add.OfficeSite = OfficeSite
                    doctor_add.WorkTime = WorkTime
                    doctor_add.Education = Education
                    doctor_add.Introduce = Introduce
                    doctor_add.Achievements = Achievements
                    doctor_add.Characters = Characters
                    doctor_add.Category = "医生"
                    doctor_add.save()
                    messages.error(request,'添加成功。')
                    return render(request,'DoctorInfQuery.html')
            except:
                return render(request,'DoctorInfAdd.html')
        return render(request,'DoctorInfAdd.html')


"""医生信息编辑"""
def DoctorInfEdit(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method  == "POST":
            DoctorID = request.POST.get("DoctorID",None)
            Name = request.POST.get("Name",None)
            Sex = request.POST.get("Sex",None)
            Age = int(request.POST.get("Age",None))
            Photo = request.POST.get("Photo",None)
            Tel = request.POST.get("Tel",None)
            Position = request.POST.get("Position",None)
            Office = request.POST.get("Office",None)
            OfficeSite = request.POST.get("OfficeSite",None)
            WorkTime = request.POST.get("WorkTime",None)
            Education = request.POST.get("Education",None)
            Introduce = request.POST.get("Introduce",None)
            Achievements = request.POST.get("Achievements",None)
            Characters = request.POST.get("Characters",None)
            try:
                # 判断医生编号是否合法
                if len(DoctorID) != 9 or not DoctorID.isdigit():
                    messages.error(request,'医生编号不符合规范，请重新输入。')
                    return render(request,'DoctorInfAdd.html')
                # 判断年龄是否合法
                elif Age < 0:
                    messages.error(request,'年龄应＞0，请重新输入')
                    return render(request,'DoctorInfAdd.html')
                # 判断电话是否合法
                elif len(Tel) != 11 and is_have_alpha(Tel):
                    messages.error(request,'电话号码不符合规范，请从新输入。')
                    return render(request,'DoctorInfAdd.html')
                else:
                    tmp = models.DoctorInf.objects.get(DoctorID = DoctorID)
                    tmp.DoctorID = DoctorID
                    tmp.Name = Name
                    tmp.Sex = Sex
                    tmp.Age = Age
                    tmp.Photo = Photo
                    tmp.Tel = Tel
                    tmp.Position = Position
                    tmp.Office = Office
                    tmp.OfficeSite = OfficeSite
                    tmp.WorkTime = WorkTime
                    tmp.Education = Education
                    tmp.Introduce = Introduce
                    tmp.Achievements = Achievements
                    tmp.Characters = Characters
                    tmp.Category = "医生"
                    tmp.save()
                    messages.error(request,'修改成功。')
                    return render(request,'DoctorInfQuery.html')
            except:
                return render(request,'DoctorInfQuery.html')
        return render(request,'DoctorInfEdit.html')
    

"""医生信息详细"""
def DoctorInfDetail(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        DoctorID = request.GET.get("id")
        tmp = models.DoctorInf.objects.filter(DoctorID = DoctorID)
        return render(request,'DoctorInfDetail.html',{'SearchInf':tmp})


"""医生信息可视化"""
def DoctorInfVisualization(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        tmp = models.DoctorInf.objects.all()
        # 存储科室名称
        office_name = []
        # 存储各个科室人数
        office_number = []
        # 存储学历名称
        education_name = []
        # 存储职称名称
        position_name = []
        # 存储个职称人数
        position_number = []
        # 存储学历人数
        education_number = []
        # 存储图表1返回数据
        office_data_back = []
        # 存储图表2返回数据
        position_data_back = []
        # 存储图表3返回数据
        education_data_back = []
        for i in tmp:
            office_name.append(i.Office)
            position_name.append(i.Position)
            education_name.append(i.Education)
        # 科室名称去重
        office_name = list(set(office_name))
        # 职称名称去重
        position_name = list(set(position_name))
        # 学历名称去重
        education_name = list(set(education_name))
        for i in office_name:
            office_number.append(models.DoctorInf.objects.filter(Office = i).count())
        for i in position_name:
            position_number.append(models.DoctorInf.objects.filter(Position = i).count())
        for i in education_name:
            education_number.append(models.DoctorInf.objects.filter(Education = i).count())
        for i in range(len(office_name)):
            office_data_back.append([office_name[i],office_number[i]])
        for i in range(len(position_name)):
            position_data_back.append({'name':position_name[i],'y':position_number[i]})
        for i in range(len(education_name)):
            education_data_back.append({'name':education_name[i],'y':education_number[i]})
        return render(request,'DoctorInfVisualization.html',{'office_data_back':office_data_back,'position_data_back':position_data_back,'education_data_back':education_data_back})


"""药物信息查询"""
def DrugInfQuery(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":    
            SearchWd = request.POST.get('SearchWd',None)
            try:
                if SearchWd == "":
                    tmp = models.DrugInf.objects.all().order_by("DrugID")
                    return render(request,'DrugInfQUery.html',{'SearchInf':tmp})
                # 查询药物编号
                elif len(SearchWd) == 5 and SearchWd.isdigit():
                    tmp = models.DrugInf.objects.filter(DrugID = SearchWd).order_by("DrugID")
                    return render(request,'DrugInfQUery.html',{'SearchInf':tmp})
                else:
                    # 查询药物名称
                    if models.DrugInf.objects.filter(DrugName = SearchWd):
                        tmp = models.DrugInf.objects.filter(DrugName = SearchWd).order_by("DrugID")
                        return render(request,'DrugInfQUery.html',{'SearchInf':tmp})
                    # 查询供货单位
                    else:
                        tmp = models.DrugInf.objects.filter(DeliveryUnit = SearchWd).order_by("DrugID")
                        return render(request,'DrugInfQUery.html',{'SearchInf':tmp})
            except:
                return render(request,'DrugInfQuery.html')
        elif request.method == "GET":
            method = request.GET.get("method")
            DrugID = request.GET.get("id")
            # 1表示删除
            if method == "1":
                tmp = models.DrugInf.objects.get(DrugID = DrugID)
                if tmp.DrugNum > 0:
                    messages.error(request,"该药物数量不为零，删除失败。")
                else:
                    messages.error(request,"删除成功。")
                    tmp.delete()
                tmp = models.DrugInf.objects.all().order_by("DrugID")
                return render(request,'DrugInfQuery.html',{'SearchInf':tmp})
            # 2表示编辑
            elif method == "2":
                tmp = models.DrugInf.objects.filter(DrugID = DrugID)
                return render(request,'DrugInfEdit.html',{'SearchInf':tmp})
        return render(request,'DrugInfQuery.html')


"""药物信息添加"""
def DrugInfAdd(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            DrugID = request.POST.get("DrugID",None)
            Specs = request.POST.get("Specs",None)
            Component = request.POST.get("Component",None)
            Character = request.POST.get("Character",None)
            Indication = request.POST.get("Indication",None)
            Usage = request.POST.get("Usage",None)
            SideEffect = request.POST.get("SideEffect",None)
            Taboo = request.POST.get("Taboo",None)
            Note = request.POST.get("Note",None)
            Gravida = request.POST.get("Gravida",None)
            ChildDrug = request.POST.get("ChildDrug",None)
            OlderDrug = request.POST.get("OlderDrug",None)
            DrugInteraction = request.POST.get("DrugInteraction",None)
            DrugToxicology = request.POST.get("DrugToxicology",None)
            Store = request.POST.get("Store",None)
            Packing = request.POST.get("Packing",None)
            ExecutiveStard = request.POST.get("ExecutiveStard",None)
            DrugOverdose = request.POST.get("DrugOverdose",None)
            try:
                # 药品已存在，允许更新其他数据
                if models.DrugInf.objects.filter(DrugID = DrugID):
                    tmp = models.DrugInf.objects.get(DrugID = DrugID)
                    tmp.Specs = Specs
                    tmp.Component = Component
                    tmp.Character = Character
                    tmp.Indication = Indication
                    tmp.Usage = Usage
                    tmp.SideEffect = SideEffect
                    tmp.Taboo = Taboo
                    tmp.Note = Note
                    tmp.Gravida = Gravida
                    tmp.ChildDrug = ChildDrug
                    tmp.OlderDrug = OlderDrug
                    tmp.DrugInteraction = DrugInteraction
                    tmp.DrugToxicology =DrugToxicology
                    tmp.Store = Store
                    tmp.Packing = Packing
                    tmp.ExecutiveStard = ExecutiveStard
                    tmp.DrugOverdose = DrugOverdose
                    tmp.Flag = "1"
                    tmp.save()
                    messages.error(request,'添加成功。')
                    return render(request,'DrugInfQuery.html')
                else:
                    messages.error(request,'该药物编号不存在。')
                    return render(request,'DrugInfAdd.html')
            except:
                return render(request,'DrugInfAdd.html')
        return render(request,'DrugInfAdd.html')


"""药品信息编辑"""
def DrugInfEdit(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            DrugID = request.POST.get("DrugID",None)
            Specs = request.POST.get("Specs",None)
            Component = request.POST.get("Component",None)
            Character = request.POST.get("Character",None)
            Indication = request.POST.get("Indication",None)
            Usage = request.POST.get("Usage",None)
            SideEffect = request.POST.get("SideEffect",None)
            Taboo = request.POST.get("Taboo",None)
            Note = request.POST.get("Note",None)
            Gravida = request.POST.get("Gravida",None)
            ChildDrug = request.POST.get("ChildDrug",None)
            OlderDrug = request.POST.get("OlderDrug",None)
            DrugInteraction = request.POST.get("DrugInteraction",None)
            DrugToxicology = request.POST.get("DrugToxicology",None)
            Store = request.POST.get("Store",None)
            Packing = request.POST.get("Packing",None)
            ExecutiveStard = request.POST.get("ExecutiveStard",None)
            DrugOverdose = request.POST.get("DrugOverdose",None)
            try:
                tmp = models.DrugInf.objects.get(DrugID = DrugID)
                tmp.Specs = Specs
                tmp.Specs = Specs
                tmp.Component = Component
                tmp.Character = Character
                tmp.Indication = Indication
                tmp.Usage = Usage
                tmp.SideEffect = SideEffect
                tmp.Taboo = Taboo
                tmp.Note = Note
                tmp.Gravida = Gravida
                tmp.ChildDrug = ChildDrug
                tmp.OlderDrug = OlderDrug
                tmp.DrugInteraction = DrugInteraction
                tmp.DrugToxicology =DrugToxicology
                tmp.Store = Store
                tmp.Packing = Packing
                tmp.ExecutiveStard = ExecutiveStard
                tmp.DrugOverdose = DrugOverdose
                tmp.Flag = "1"
                tmp.save()
                messages.error(request,'添加成功。')
                return render(request,'DrugInfQuery.html')
            except:
                return render(request,'DrguInfQuery.html')
        return render(request,'DrugInfQUery.html')


"""药品信息详细"""
def DrugInfDetail(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "GET":
            DrugID = request.GET.get('id',None)
            tmp = models.DrugInf.objects.filter(DrugID = DrugID)
            return render(request,'DrugInfDetail.html',{'SearchInf':tmp})


"""药品信息可视化"""
def DrugInfVisualization(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        tmp = models.DrugInf.objects.all()
        # 存储药品名称
        drug_name = []
        # 存储药品数量
        drug_number = []
        # 存储返回数据
        data_back = []
        for i in tmp:
            drug_name.append(i.DrugID+"-"+i.DrugName)
        for i in drug_name:
            tmp  = models.DrugInf.objects.filter(DrugID = i[:5])
            drug_number.append(tmp[0].DrugNum)
        for i in range(len(drug_name)):
            data_back.append({'name':drug_name[i],'y':drug_number[i]})
        return render(request,'DrugInfVisualization.html',{'data_back':data_back})


"""病例信息查询"""
def CaseInfQuery(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            SearchWd = request.POST.get('SearchWd',None)
            try:
                if SearchWd == "":
                    tmp = models.CaseInf.objects.all().order_by("CaseID")
                    return render(request,'CaseInfQuery.html',{'SearchInf':tmp})
                # 查询病例编号
                elif SearchWd[0] == "C" and SearchWd[1:].isdigit():
                    tmp = models.CaseInf.objects.filter(CaseID = SearchWd).order_by("CaseID")
                    return render(request,'CaseInfQuery.html',{'SearchInf':tmp})
                # 查询宠物证编号
                elif SearchWd[0] == "P" and SearchWd[1:].isdigit():
                    tmp = models.CaseInf.objects.filter(PetCardID = SearchWd).order_by("CaseID")
                    return render(request,'CaseInfQuery.html',{'SearchInf':tmp})
                # 查询宠物主姓名
                else:
                    tmp = models.CaseInf.objects.filter(PetOwnerName = SearchWd).order_by("CaseID")
                    return render(request,'CaseInfQuery.html',{'SearchInf':tmp})
            except:
                return render(request,'CaseInfQuery.html')
        elif request.method == "GET":
            method = request.GET.get("method")
            CaseID = request.GET.get("id")
            # 1表示删除
            if method == "1":
                models.CaseInf.objects.filter(CaseID = CaseID).delete()
                tmp = models.CaseInf.objects.all().order_by("CaseID")
                messages.error(request,'删除成功。')
                return render(request,'CaseInfQuery.html',{'SearchInf':tmp})  
            # 2表示编辑
            elif method == "2":
                tmp = models.CaseInf.objects.filter(CaseID = CaseID).order_by("CaseID")
                return render(request,'CaseInfEdit.html',{'SearchInf':tmp})
        return render(request,'CaseInfQuery.html')


"""病例信息添加"""
def CaseInfAdd(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            CaseID = request.POST.get("CaseID",None)
            PetOwnerName = request.POST.get("PetOwnerName",None)
            Tel = request.POST.get("Tel",None)
            DoctorID  = request.POST.get("DoctorID",None)
            PetOwnerSex = request.POST.get("PetOwnerSex",None)
            PostCode = request.POST.get("PostCode",None)
            Address = request.POST.get("Address",None)
            Email = request.POST.get("Email",None)
            PetName = request.POST.get("PetName",None)
            PetCardID = request.POST.get("PetCardID",None)
            Breed = request.POST.get("Breed",None)
            PetSex = request.POST.get("PetSex",None)
            PetAge = int(request.POST.get("PetAge",None))
            PetWeight = float(request.POST.get("PetWeight",None))
            Immune = request.POST.get("Immune",None)
            Sterilization = request.POST.get("Sterilization",None)
            TotalSum = float(request.POST.get("TotalSum",None))
            Treatment = request.POST.get('Treatment',None)
            Prescription = request.POST.get("Prescription",None)
            try:
                # 判断病例编号是否已存在
                if models.CaseInf.objects.filter(CaseID = CaseID):
                    messages.error(request,'病例编号重复，请重新输入。')
                    return render(request,'CaseInfAdd.html')
                # 判断病例编号是否合法
                elif len(CaseID) != 12 or CaseID[0] != "C" or is_have_alpha(CaseID[1:]):
                    messages.error(request,'病例编号不符合规范，请重新输入。')
                    return render(request,'CaseInfAdd.html')
                # 判断电话号码是否合法
                elif len(Tel) != 11 or is_have_alpha(Tel):
                    messages.error(request,'电话号码不符合规范，请重新输入。')
                    return render(request,'CaseInfAdd.html')
                # 判断医生编号是否存在
                elif not models.DoctorInf.objects.filter(DoctorID = DoctorID):
                    messages.error(request,'医生编号不存在，请重新输入。')
                    return render(request,'CaseInfAdd.html')
                # 判断邮编是否合法
                elif len(PostCode) != 6 or is_have_alpha(PostCode):
                    messages.error(request,'邮编不符合规范，请重新输入。')
                    return render(request,'CaseInfAdd.html')
                # 判断宠物证是否合法
                elif len(PetCardID) != 12 or PetCardID[0] != "P" or is_have_alpha(PetCardID[1:]):
                    messages.error(request,'宠物证编号不符合规范，请重新输入。')
                    return render(request,'CaseInfAdd.html')
                # 判断宠物年龄是否合法
                elif PetAge < 0 or PetAge > 50:
                    messages.error(request,'宠物年龄应＞0，请重新输入。')
                    return render(request,'CaseInfAdd.html')
                # 判断宠物体重是否合法
                elif PetWeight < 0 or PetWeight > 500:
                    messages.error(request,'宠物体重应＞0，请重新输入。')
                    return render(request,'CaseInfAdd.html')
                # 判断宠物总金额是否合法
                elif TotalSum < 0 :
                    messages.error(request,'总金额应≥0，请重新输入。')
                    return render(request,'CaseInfAdd.html')
                else:
                    case_add = models.CaseInf()
                    case_add.CaseID = CaseID
                    case_add.PetOwnerName = PetOwnerName
                    case_add.Tel = Tel
                    case_add.DoctorID = DoctorID
                    case_add.PetOwnerSex = PetOwnerSex
                    case_add.PostCode = PostCode
                    case_add.Address = Address
                    case_add.Email = Email
                    case_add.PetName = PetName
                    case_add.PetCardID = PetCardID
                    case_add.Breed = Breed
                    case_add.PetSex = PetSex
                    case_add.PetAge = PetAge
                    case_add.PetWeight = PetWeight
                    case_add.Immune = Immune
                    case_add.Sterilization = Sterilization
                    case_add.TotalSum = TotalSum
                    case_add.Treatment = Treatment
                    case_add.Prescription = Prescription
                    case_add.save()
                    messages.error(request,'添加成功。')
            except:
                return render(request,'CaseInfAdd.html')
        return render(request,'CaseInfAdd.html')


"""病例信息编辑"""
def CaseInfEdit(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "POST":
            CaseID = request.POST.get("CaseID",None)
            PetOwnerName = request.POST.get("PetOwnerName",None)
            Tel = request.POST.get("Tel",None)
            DoctorID  = request.POST.get("DoctorID",None)
            PetOwnerSex = request.POST.get("PetOwnerSex",None)
            PostCode = request.POST.get("PostCode",None)
            Address = request.POST.get("Address",None)
            Email = request.POST.get("Email",None)
            PetName = request.POST.get("PetName",None)
            PetCardID = request.POST.get("PetCardID",None)
            Breed = request.POST.get("Breed",None)
            PetSex = request.POST.get("PetSex",None)
            PetAge = int(request.POST.get("PetAge",None))
            PetWeight = float(request.POST.get("PetWeight",None))
            Immune = request.POST.get("Immune",None)
            Sterilization = request.POST.get("Sterilization",None)
            TotalSum = float(request.POST.get("TotalSum",None))
            Treatment = request.POST.get('Treatment',None)
            Prescription = request.POST.get("Prescription",None)
            try:
                # 判断病例编号是否合法
                if len(CaseID) != 12 or CaseID[0] != "C" or is_have_alpha(CaseID[1:]):
                    messages.error(request,'病例编号不符合规范，请重新输入。')
                    return render(request,'CaseInfEdit.html')
                # 判断电话号码是否合法
                elif len(Tel) != 11 or is_have_alpha(Tel):
                    messages.error(request,'电话号码不符合规范，请重新输入。')
                    return render(request,'CaseInfEdit.html')
                # 判断邮编是否合法
                elif len(PostCode) != 6 or is_have_alpha(PostCode):
                    messages.error(request,'邮编不符合规范，请重新输入。')
                    return render(request,'CaseInfEdit.html')
                # 判断宠物证是否合法
                elif len(PetCardID) != 12 or PetCardID[0] != "P" or is_have_alpha(PetCardID[1:]):
                    messages.error(request,'宠物证编号不符合规范，请重新输入。')
                    return render(request,'CaseInfEdit.html')
                # 判断宠物年龄是否合法
                elif PetAge < 0 or PetAge > 50:
                    messages.error(request,'宠物年龄应＞0，请重新输入。')
                    return render(request,'CaseInfEdit.html')
                # 判断宠物体重是否合法
                elif PetWeight < 0 or PetWeight > 500:
                    messages.error(request,'宠物体重应＞0，请重新输入。')
                    return render(request,'CaseInfEdit.html')
                # 判断宠物总金额是否合法
                elif TotalSum < 0 :
                    messages.error(request,'总金额应≥0，请重新输入。')
                    return render(request,'CaseInfEdit.html')
                else:
                    tmp = models.CaseInf.objects.get(CaseID = CaseID)
                    tmp.PetOwnerName = PetOwnerName
                    tmp.PetOwnerSex = PetOwnerSex
                    tmp.Tel = Tel
                    tmp.Email = Email
                    tmp.PostCode  = PostCode
                    tmp.Address = Address
                    tmp.PetName = PetName
                    tmp.Breed = Breed 
                    tmp.PetSex = PetSex
                    tmp.PetAge = PetAge
                    tmp.PetWeight = PetWeight
                    tmp.Immune = Immune
                    tmp.Sterilization = Sterilization
                    tmp.PetCardID = PetCardID
                    tmp.DoctorID = DoctorID
                    tmp.Treatment = Treatment
                    tmp.Prescription = Prescription
                    tmp.TotalSum = TotalSum
                    tmp.save()
                    messages.error(request,'修改成功。')
                    return render(request,'CaseInfQuery.html')
            except:
                return render(request,'CaseInfQuery.html')     
        return render(request,'CaseInfQuery.html')


"""病例信息详细"""
def CaseInfDetail(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        if request.method == "GET":
            CaseID = request.GET.get("id")
            tmp = models.CaseInf.objects.filter(CaseID = CaseID)
            return render(request,'CaseInfDetail.html',{'SearchInf':tmp})


"""病例信息可视化"""
def CaseInfVisualization(request):
    # 判断sesssion是否含有该键值对,以及判断该该值是否存在在数据库中
    if ('id' not in request.session.keys()) or (len(models.ManagerInf.objects.filter(ManagerID = request.session['id'])) == 0):
        register_form = UserForm(request.POST)
        messages.error(request,'请先登录。')
        return render(request,'LogIn.html',{'register_form':register_form})
    # 判断id对应值是否为管理员帐号
    else:
        tmp = models.CaseInf.objects.all()
        # 宠物种类
        breeds = []
        # 宠物数量
        number1 = []
        # 种类-数量 数据组合
        BreedNumber = []
        # 免疫情况
        immunes = []
        # 免疫数量/未免疫数量
        number2 = []
        # 免疫情况-数量 数据组合
        ImmuneNumber = []
        # 绝育情况
        sterilization = []
        # 绝育数量/为绝育数量
        number3 = []
        # 绝育情况-数量 数据组合
        SterilizationNumber = []

        for i in range(len(tmp)):
            breeds.append(tmp[i].Breed)
            immunes.append(tmp[i].Immune)
            sterilization.append(tmp[i].Sterilization)

        # 宠物种类去重
        breeds = list(set(breeds))
        # 宠物免疫情况去重
        immunes = list(set(immunes))
        # 宠物绝育情况去重
        sterilization = list(set(sterilization))

        for i in breeds:
            tmp = models.CaseInf.objects.filter(Breed = i)
            number1.append(len(tmp))
        for i in immunes:
            tmp = models.CaseInf.objects.filter(Immune = i)
            number2.append(len(tmp))
        for i in sterilization:
            tmp = models.CaseInf.objects.filter(Sterilization = i)
            number3.append(len(tmp))

        for i in range(len(breeds)):
            BreedNumber.append([breeds[i],number1[i]])
        for i in range(len(immunes)):
            ImmuneNumber.append({'name':immunes[i],'y':number2[i]})
        for i in range(len(sterilization)):
            SterilizationNumber.append({'name':sterilization[i],'y':number3[i]})
        return render(request,'CaseInfVisualization.html',{'BreedNumber':BreedNumber,'ImmuneNumber':ImmuneNumber,'SterilizationNumber':SterilizationNumber})
