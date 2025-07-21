
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse
import numpy as np




import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# Create your views here.
from Remote_User.models import ClientRegister_Model,cardiac_arrest_prediction,detection_ratio,detection_accuracy,contact_details


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if (admin == "Admin" and password =="Admin")or (admin == "Ajay" and password =="Ajay"):
            detection_accuracy.objects.all().delete()
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def View_Prediction_Of_Cardiac_Arrest_Type_Ratio(request):
    detection_ratio.objects.all().delete()
    ratio = ""
    kword = 'No Cardiac Arrest Found'
    print(kword)
    obj = cardiac_arrest_prediction.objects.all().filter(Q(Prediction=kword))
    obj1 = cardiac_arrest_prediction.objects.all()
    if len(obj1)<1:
        return render(request,'SProvider/No_Predictions_Ratio.html',{'obj':"NO PREDICTIONS"})
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio.objects.create(names=kword, ratio=ratio)

    ratio1 = ""
    kword1 = 'Cardiac Arrest Found'
    print(kword1)
    obj1 = cardiac_arrest_prediction.objects.all().filter(Q(Prediction=kword1))
    obj11 = cardiac_arrest_prediction.objects.all()
    count1 = obj1.count();
    count11 = obj11.count();
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio.objects.create(names=kword1, ratio=ratio1)
    obj = detection_ratio.objects.all()
    obj=list(enumerate(obj))
    return render(request, 'SProvider/View_Prediction_Of_Cardiac_Arrest_Type_Ratio.html', {'objs': obj})

def View_Remote_Users(request):
    search_by = request.POST.get('search_by')
    search_query = request.POST.get('search_query')
    
    if search_by and search_query:
        if search_by == 'None':
            objects = ClientRegister_Model.objects.all()
        elif search_by == 'fullname':
            objects = ClientRegister_Model.objects.filter(fullname__istartswith=search_query)
        elif search_by == 'username':
            objects = ClientRegister_Model.objects.filter(username__istartswith=search_query)
        elif search_by == 'email':
            objects = ClientRegister_Model.objects.filter(email__istartswith=search_query)
        elif search_by == 'phoneno':
            objects = ClientRegister_Model.objects.filter(phoneno__istartswith=search_query)
        elif search_by == 'country':
            objects = ClientRegister_Model.objects.filter(country__istartswith=search_query)
        elif search_by == 'state':
            objects = ClientRegister_Model.objects.filter(state__istartswith=search_query)
        elif search_by == 'city':
            objects = ClientRegister_Model.objects.filter(city__istartswith=search_query)
    else:
        objects = ClientRegister_Model.objects.all()
    Count=len(objects)
    objects=list(enumerate(objects))
    return render(request, 'SProvider/View_Remote_Users.html', {'objects': objects,'Count':Count})

def contact_view(request):
    obj=contact_details.objects.all()
    Count=len(obj)
    obj = list(enumerate(obj or []))
    return render(request,'SProvider/User_Messages.html',{'objects':obj,'Count':Count})

def edit_details(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.filter(id= userid)
    if request.method=="POST":
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        phoneno=request.POST.get('phoneno')
        country=request.POST.get('country')
        state=request.POST.get('state')
        city=request.POST.get('city')
        obj=obj.update(fullname=fullname,email=email,phoneno=phoneno,country=country,state=state,city=city)
        enter = ClientRegister_Model.objects.get(id=userid)
        request.session["userid"] = enter.id
        return redirect('ViewYourProfile')
    else:
        object = ClientRegister_Model.objects.get(id= userid)
        return render(request,'Ruser/Edit_Your_Profile.html',{'object':object})

def ViewTrendings(request):
    topic = cardiac_arrest_prediction.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def charts(request,chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def View_Prediction_Of_Cardiac_Arrest_Type(request):
    search_by=request.POST.get('search_by')
    search_query=request.POST.get('search_query')
    if search_by and search_query:
        if search_by == 'None':
            obj = cardiac_arrest_prediction.objects.all()
        elif search_by == 'Fid':
            obj = cardiac_arrest_prediction.objects.filter(Fid__icontains=search_query)
        elif search_by == 'Age_In_Days':
            obj = cardiac_arrest_prediction.objects.filter(Age_In_Days__icontains=search_query)
        elif search_by == 'Sex':
            obj = cardiac_arrest_prediction.objects.filter(Sex__icontains=search_query)
        elif search_by == 'ChestPainType':
            obj = cardiac_arrest_prediction.objects.filter(ChestPainType__icontains=search_query)
        elif search_by == 'RestingBP':
            obj = cardiac_arrest_prediction.objects.filter(RestingBP__icontains=search_query)
        elif search_by == 'RestingECG':
            obj = cardiac_arrest_prediction.objects.filter(RestingECG__icontains=search_query)
        elif search_by == 'MaxHR':
            obj = cardiac_arrest_prediction.objects.filter(MaxHR__icontains=search_query)
        elif search_by == 'ExerciseAngina':
            obj = cardiac_arrest_prediction.objects.filter(ExerciseAngina__icontains=search_query)
        elif search_by == 'Oldpeak':
            obj = cardiac_arrest_prediction.objects.filter(Oldpeak__icontains=search_query)
        elif search_by == 'ST_Slope':
            obj = cardiac_arrest_prediction.objects.filter(ST_Slope__icontains=search_query)
        elif search_by == 'slp':
            obj = cardiac_arrest_prediction.objects.filter(slp__icontains=search_query)
        elif search_by == 'caa':
            obj = cardiac_arrest_prediction.objects.filter(caa__icontains=search_query)
        elif search_by == 'thall':
            obj = cardiac_arrest_prediction.objects.filter(thall__icontains=search_query)
        elif search_by == 'Prediction':
            obj = cardiac_arrest_prediction.objects.filter(Prediction__istartswith=search_query)
    else:
        obj = cardiac_arrest_prediction.objects.all()
    if len(obj)<1:
        return render(request,'SProvider/No_Predictions.html',{'obj':"NO PREDICTIONS"})
    Count=len(obj)
    obj=list(enumerate(obj))
    return render(request, 'SProvider/View_Prediction_Of_Cardiac_Arrest_Type.html', {'list_objects': obj,'Count':Count})

def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


def Download_Predicted_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Predicted_Data.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = cardiac_arrest_prediction.objects.all()
    ws.write(row_num, 0,'Fid', font_style)
    ws.write(row_num, 1,'Age_In_Days', font_style)
    ws.write(row_num, 2,'Sex', font_style)
    ws.write(row_num, 3,'ChestPainType', font_style)
    ws.write(row_num, 4,'RestingBP', font_style)
    ws.write(row_num, 5,'RestingECG', font_style)
    ws.write(row_num, 6,'MaxHR', font_style)
    ws.write(row_num, 7,'ExerciseAngina', font_style)
    ws.write(row_num, 8,'Oldpeak', font_style)
    ws.write(row_num, 9,'ST_Slope', font_style)
    ws.write(row_num, 10,'slp', font_style)
    ws.write(row_num, 11,'caa', font_style)
    ws.write(row_num, 12,'thall', font_style)
    ws.write(row_num, 13,'Prediction', font_style)

    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.Fid, font_style)
        ws.write(row_num, 1, my_row.Age_In_Days, font_style)
        ws.write(row_num, 2, my_row.Sex, font_style)
        ws.write(row_num, 3, my_row.ChestPainType, font_style)
        ws.write(row_num, 4, my_row.RestingBP, font_style)
        ws.write(row_num, 5, my_row.RestingECG, font_style)
        ws.write(row_num, 6, my_row.MaxHR, font_style)
        ws.write(row_num, 7, my_row.ExerciseAngina, font_style)
        ws.write(row_num, 8, my_row.Oldpeak, font_style)
        ws.write(row_num, 9, my_row.ST_Slope, font_style)
        ws.write(row_num, 10, my_row.slp, font_style)
        ws.write(row_num, 11, my_row.caa, font_style)
        ws.write(row_num, 12, my_row.thall, font_style)
        ws.write(row_num, 13, my_row.Prediction, font_style)

    wb.save(response)
    return response

def Download_remote_user_dataset(request):
    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Remote_Users.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj=ClientRegister_Model.objects.all()
    data = obj  # dummy method to fetch data.
    ws.write(row_num, 0, 'fullname', font_style)
    ws.write(row_num, 1, 'username', font_style)
    ws.write(row_num, 2, 'email', font_style)
    ws.write(row_num, 3, 'phoneno', font_style)
    ws.write(row_num, 4, 'country', font_style)
    ws.write(row_num, 5, 'state', font_style)
    ws.write(row_num, 6, 'city', font_style)
    
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.fullname, font_style)
        ws.write(row_num, 1, my_row.username, font_style)
        ws.write(row_num, 2, my_row.email, font_style)
        ws.write(row_num, 3, my_row.phoneno, font_style)
        ws.write(row_num, 4, my_row.country, font_style)
        ws.write(row_num, 5, my_row.state, font_style)
        ws.write(row_num, 6, my_row.city, font_style)
    
    wb.save(response)
    return response

def train_model(request):
    detection_accuracy.objects.all().delete()

    data=pd.read_csv('D:\Pandas\Datasets.csv')

    #String Columns label Encoding
    df_String=data[['Sex','ChestPainType','RestingECG','ExerciseAngina','ST_Slope']]
    df_String['id']=np.array([i for i in range(len(data))])
    for i in df_String.columns:
        df_String[i]=LabelEncoder().fit_transform(df_String[i])

    #Numerical Column 
    df_Numerical=data[['Age_In_Days','RestingBP','MaxHR','Oldpeak','slp','caa','thall','HeartDisease']]

    #Create an id column for the df_Numerical DataFrame for merging.
    df_Numerical['id']=df_String['id']

    #Merging df_String and df_Numerical,with same column id
    df_Str_Num=pd.merge(df_String,df_Numerical,on='id',how='inner')
    df_Heart_Disease=df_Str_Num['HeartDisease']

    ss=StandardScaler()
    ss1=StandardScaler()
    df_train_test=ss.fit_transform(df_Str_Num.drop(['id','HeartDisease'],axis=1))
    ss1.fit(df_Str_Num.drop(['id','HeartDisease'],axis=1))
    df_train_test=pd.DataFrame(df_train_test,columns=['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope', 'Age_In_Days', 'RestingBP', 'MaxHR', 'Oldpeak', 'slp', 'caa','thall'])

    #x,y cariables
    x=df_train_test
    y=df_Heart_Disease
    

    models = []
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25,random_state=42)

    print("Random Forest Classifier")
    rfc = RandomForestClassifier()
    rfc.fit(X_train, y_train)
    y_pred = rfc.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, y_pred) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, y_pred))
    models.append(('RandomForestClassifier', rfc))
    detection_accuracy.objects.create(names="RandomForest Classifier",
                                      ratio=accuracy_score(y_test, y_pred) * 100)


    # SVM Model
    print("SVM")
    lin_clf =LinearSVC()
    lin_clf.fit(X_train, y_train)
    predict_svm = lin_clf.predict(X_test)
    svm_acc = accuracy_score(y_test, predict_svm) * 100
    print("ACCURACY")
    print(svm_acc)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, predict_svm))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, predict_svm))
    detection_accuracy.objects.create(names="Support Vector Machine", ratio=svm_acc)

    print("Logistic Regression")
    reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, y_pred) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, y_pred))
    detection_accuracy.objects.create(names="Logistic Regression", ratio=accuracy_score(y_test, y_pred) * 100)

    print("Decision Tree Classifier")
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    dtcpredict = dtc.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, dtcpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, dtcpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, dtcpredict))
    print(x)
    detection_accuracy.objects.create(names="Decision Tree Classifier", ratio=accuracy_score(y_test, dtcpredict) * 100)

    labeled = 'labeled_data.csv'
    data.to_csv(labeled, index=False)
    data.to_markdown

    obj = detection_accuracy.objects.all()
    obj=list(enumerate(obj))
    return render(request,'SProvider/train_model.html', {'objs': obj})