from django.urls import path
from User.views import Registerview,Loginview,Userview,Logoutview,CRUDoperations,Employeesalaryview

urlpatterns = [
    path('register/', Registerview.as_view(), name='register'),
    path('login/', Loginview.as_view(), name='login'),
    path('user/', Userview.as_view(), name='user'),
    path('logout/', Logoutview.as_view(), name='logout'),
    path('crud/', CRUDoperations.as_view(), name='crud'),
    path('crud/<str:Emp_no>/', CRUDoperations.as_view(), name='crud'),
    path('nested/',Employeesalaryview.as_view(), name='nested'),
    path('nested/<str:Emp_no>/',Employeesalaryview.as_view(), name='nested'),
]
