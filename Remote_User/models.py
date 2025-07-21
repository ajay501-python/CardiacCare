from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    fullname=models.CharField(max_length=30,blank=False,null=False)
    username = models.CharField(max_length=30,unique=True,blank=False,null=False)
    email = models.EmailField(max_length=30,blank=False,null=False)
    password = models.CharField(max_length=10,blank=False,null=False)
    phoneno = models.CharField(max_length=10,blank=False,null=False)
    country = models.CharField(max_length=30,blank=False,null=False)
    state = models.CharField(max_length=30,blank=False,null=False)
    city = models.CharField(max_length=30,blank=False,null=False)


class cardiac_arrest_prediction(models.Model):

    Fid= models.CharField(max_length=3000,blank=True,null=False)
    Age_In_Days= models.CharField(max_length=3000,blank=False,null=False)
    Sex= models.CharField(max_length=3000,blank=False,null=False)
    ChestPainType= models.CharField(max_length=3000,blank=False,null=False)
    RestingBP= models.CharField(max_length=3000,blank=False,null=False)
    RestingECG= models.CharField(max_length=3000,blank=False,null=False)
    MaxHR= models.CharField(max_length=3000,blank=False,null=False)
    ExerciseAngina= models.CharField(max_length=3000,blank=False,null=False)
    Oldpeak= models.CharField(max_length=3000,blank=False,null=False)
    ST_Slope= models.CharField(max_length=3000,blank=False,null=False)
    slp= models.CharField(max_length=3000,blank=False,null=False)
    caa= models.CharField(max_length=3000,blank=False,null=False)
    thall= models.CharField(max_length=3000,blank=False,null=False)
    Prediction= models.CharField(max_length=3000,blank=False,null=False)


class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)


class forgot_password(models.Model):
    username=models.CharField(max_length=300,unique=True)
    email=models.EmailField(max_length=300)
    sending_otp=models.CharField(max_length=300)

class contact_details(models.Model):
    fullname=models.CharField(max_length=300)
    email=models.EmailField(max_length=300)
    subject=models.CharField(max_length=20)
    message=models.CharField(max_length=300)