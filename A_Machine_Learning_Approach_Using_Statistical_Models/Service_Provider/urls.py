from django.urls import path
from .views import *

urlpatterns=[
    path('serviceproviderlogin/',serviceproviderlogin, name="serviceproviderlogin"),
    path('View_Remote_Users/',View_Remote_Users,name="View_Remote_Users"),
    path('contact_view/',contact_view,name="contact_view"),
    path('edit_details/', edit_details, name="edit_details"),
    path('charts/(?P<chart_type>\w+)', charts,name="charts"),
    path('charts1/(?P<chart_type>\w+)', charts1, name="charts1"),
    path('likeschart/(?P<like_chart>\w+)', likeschart, name="likeschart"),
    path('View_Prediction_Of_Cardiac_Arrest_Type_Ratio/', View_Prediction_Of_Cardiac_Arrest_Type_Ratio, name="View_Prediction_Of_Cardiac_Arrest_Type_Ratio"),
    path('train_model/', train_model, name="train_model"),
    path('View_Prediction_Of_Cardiac_Arrest_Type/', View_Prediction_Of_Cardiac_Arrest_Type, name="View_Prediction_Of_Cardiac_Arrest_Type"),
    path('Download_Predicted_DataSet/', Download_Predicted_DataSets, name="Download_Predicted_DataSets"),
    path('Download_remote_user_dataset/',Download_remote_user_dataset,name="Download_remote_user_dataset")

]
