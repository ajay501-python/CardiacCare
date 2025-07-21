from django.contrib.auth import authenticate,login
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import numpy as np

from sklearn.ensemble import RandomForestClassifier
import pandas as pd

import random
import smtplib
#MIME --> Multiplication Internet MailExtention
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,cardiac_arrest_prediction,detection_ratio,detection_accuracy,forgot_password,contact_details
def home(request):
    return render(request,'RUser/home.html')

def about(request):
    return render(request,'RUser/About.html')

def Technology(request):
    return render(request,'RUser/Technology.html')

def Research(request):
    return render(request,'RUser/Research.html')

def Contacts(request):
    if request.method=="POST":
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        contact_details.objects.create(fullname=fullname,email=email,subject=subject,message=message)
        return redirect('home')
    return render(request,'RUser/Contacts.html')
    
def login(request):
    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id
            if enter.password==password:
                return redirect('ViewYourProfile')
            else:
                return redirect('login')
        except:
            pass
    return render(request,'RUser/login.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})

def Mail_Send(request,username,receiver_mail,mail_subject,Password):
            otp = ''.join([str(random.randint(0,9)) for _ in range(6)])
            sender='ajayaddanki55@gmail.com'
            pwd='gyasnikvrailwsom'
            sending_otp=otp
            receiver=receiver_mail
            subject=mail_subject
            if Password!='':
                body=f'Dear {str(username)} \n Email: {str(receiver)}  \n Password: {str(Password)}  {mail_subject}'
            else:
                body=f'Dear {str(username)} \n Email: {str(receiver)}  \n OTP: {str(sending_otp)}  {mail_subject}'
            msg=MIMEMultipart()
            msg['From']=sender
            msg['To']=receiver
            msg['subject']=subject
            msg.attach(MIMEText(body))
            text=msg.as_string()
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(sender,pwd)
            server.sendmail(subject,receiver,text)
            server.quit()
            print("Mail sent success ")
            print(f"Generated OTP: {otp}") 
            object=forgot_password.objects.filter(username=username)
            if Password:
                try:
                    enter = ClientRegister_Model.objects.get(username=username)
                    request.session["userid"] = enter.id
                except:
                    pass
            else:
                if object:
                    object=object.update(sending_otp=sending_otp)
                else:
                    object=forgot_password.objects.create(username=username,email=receiver_mail,sending_otp=sending_otp)
                try:
                    enter = ClientRegister_Model.objects.get(username=username)
                    request.session["userid"] = enter.id
                except:
                    pass
            return sending_otp

def Register(request):

    if request.method == "POST":
        fullname=request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        try:
            if len(password)<8:
                return render(request,'RUser/Register.html',{'message':'Password Min Length: 8'})
            obj=ClientRegister_Model.objects.create(fullname=fullname,username=username, email=email, password=password, phoneno=phoneno,
                                                country=country, state=state, city=city)
            otp=Mail_Send(request,username,email,'OTP For Registration',Password='')
            Mail_Send(request,username,email,'Credentials For Login',Password=password)
            obj=ClientRegister_Model.objects.get(username=username,email=email)
            request.session["userid"] = obj.id
            print('Account Created')
            return redirect('Confirm_Email')
        except Exception as e:
            print(e)
            return render(request,'Ruser/Username_Already_Exist.html',{'username':username,'email':email})
    else:
        return render(request,'RUser/Register.html')
 
def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})

def forget_password(request):
    if request.method== "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        sending_otp= Mail_Send(request,username,email,'OTP for confirm password','')
        userid = request.session['userid']
        object= ClientRegister_Model.objects.get(id= userid)
        object=forgot_password.objects.filter(username=username)
        if object:
            object=object.update(sending_otp=sending_otp)
        else:
            object=forgot_password.objects.create(username=username,email=email,sending_otp=sending_otp)
        try:
            enter = ClientRegister_Model.objects.get(username=username)
            request.session["userid"] = enter.id
            return redirect('Confirm_Password')
        except:
            return render(request,'RUser/User_Not_Found.html',{'username':username})
    else:
        return render(request,'RUser/forget_password.html')
    
def Confirm_Password(request):
    userid = request.session['userid']
    if request.method== "POST":
        username=request.POST.get('username')
        entered_otp=request.POST.get('otp')
        new_password=request.POST.get('password')
        try:
            obj1= forgot_password.objects.get(username=username)
        except:
            return render(request,'RUser/User_Not_Found.html',{'username':username})
        print(obj1.sending_otp)
        if obj1.sending_otp==entered_otp:
            ClientRegister_Model.objects.filter(id=userid).update(password=new_password)
            return render(request,'RUser/Password_Reset.html')
        else:
            return render(request,'RUser/Confirm_Password.html',{'info':'Wrong OTP'})        
    else:   
        return render(request,'RUser/Confirm_Password.html',{'info':' '})
        
        
def Confirm_Email(request):
    userid = request.session['userid']
    object= ClientRegister_Model.objects.get(id= userid)
    if request.method=="POST":
        one=request.POST.get('1')
        two=request.POST.get('2')
        three=request.POST.get('3')
        four=request.POST.get('4')
        five=request.POST.get('5')
        six=request.POST.get('6')
        print(one)
        otp=one+two+three+four+five+six
        object=forgot_password.objects.get(username=object.username)
        if object.sending_otp==str(otp):
            return render(request,'RUser/Mail_Verifed.html',{'email':object.email})
        else:
            return render(request,'RUser/Wrong_Otp.html')
    return render(request,'RUser/Confirm_Email.html',{'obj':' '})


def resend_otp(request):
    userid = request.session['userid']
    object= ClientRegister_Model.objects.get(id= userid)
    new_otp=Mail_Send(request,object.username,object.email,'OTP')
    object=forgot_password.objects.filter(username=object.username)
    if object:
        object=object.update(sending_otp=new_otp)
    else:
        object=forgot_password.objects.create(username=object.username,email=object.email,sending_otp=new_otp)
    try:
        enter = ClientRegister_Model.objects.get(username=object.username)
        request.session["userid"] = enter.id
        return redirect('Confirm_Password')
    except:
        return redirect('login')


def Best_Accuracy_Model_Result(Vector):
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

    # SVM Model
    print("SVM")
    lin_clf = LinearSVC()
    lin_clf.fit(X_train, y_train)
    predict_svm = lin_clf.predict(X_test)
    svm_acc = accuracy_score(y_test, predict_svm) * 100
    print(svm_acc)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, predict_svm))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, predict_svm))
    models.append(('svm', lin_clf))

    #Logistic Regression
    print("Logistic Regression")
    reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, y_pred) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, y_pred))
    models.append(('logistic', reg))

    
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
    models.append(('decisiontree', dtc))

    classifier = VotingClassifier(models)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    #Transform User Values into StandardScalerValues
    Vector=ss1.transform(Vector).reshape(1,-1)
    predict_text = classifier.predict(Vector)

    pred = str(predict_text).replace("[", "")
    pred1 = str(pred.replace("]", ""))

    prediction = int(pred1)

    if prediction == 0:
        val = 'No Cardiac Arrest Found'
    elif prediction == 1:
        val = 'Cardiac Arrest Found'

    print(prediction)
    print('This is an value')
    print(val)
    return val



def Predict_Cardiac_Arrest_Type(request):
    if request.method == "POST":

        if request.method == "POST":

            Fid= request.POST.get('Fid')
            Age_In_Days= request.POST.get('Age_In_Days')
            Sex= request.POST.get('Sex')
            ChestPainType= request.POST.get('ChestPainType')
            RestingBP= request.POST.get('RestingBP')
            RestingECG= request.POST.get('RestingECG')
            MaxHR= request.POST.get('MaxHR')
            ExerciseAngina= request.POST.get('ExerciseAngina')
            Oldpeak= float(request.POST.get('Oldpeak'))
            ST_Slope= request.POST.get('ST_Slope')
            slp= request.POST.get('slp')
            caa= request.POST.get('caa')
            thall= request.POST.get('thall')
        
        

        #String_Values[Sex, ChestPainType,RestingECG,ExerciseAngina,ST_Slope]
        #Numerical_Values[Age_In_Days,RestingBP, MaxHR, Oldpeak,slp, caa,thall]
        Vector_1= np.array([Sex[0], ChestPainType[0],RestingECG[0],ExerciseAngina[0],ST_Slope[0],Age_In_Days,RestingBP, MaxHR, Oldpeak,slp, caa,thall]).reshape(1,-1)[0].reshape(1,-1)
        val=Best_Accuracy_Model_Result(Vector_1)

        cardiac_arrest_prediction.objects.create(
        Fid=Fid,
        Age_In_Days=Age_In_Days,
        Sex=Sex[1:],
        ChestPainType=ChestPainType[1:],
        RestingBP=RestingBP,
        RestingECG=RestingECG[1:],
        MaxHR=MaxHR,
        ExerciseAngina=ExerciseAngina[1:],
        Oldpeak=Oldpeak,
        ST_Slope=ST_Slope[1:],
        slp=slp,
        caa=caa,
        thall=thall,
        Prediction=val)

        return render(request, 'RUser/Predict_Cardiac_Arrest_Type.html',{'objs': val})
    return render(request, 'RUser/Predict_Cardiac_Arrest_Type.html')


@login_required
def Real_Time_Alerts(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        date=request.POST.get('date')
        time=request.POST.get('time')
        alert_type=request.POST.get('alert_type')
        message=request.POST.get('message')
        print(date,time)
        return render(request,'RUser/Success_Alert.html')
    else:
        return render(request,'RUser/Real_Time_Alerts.html')