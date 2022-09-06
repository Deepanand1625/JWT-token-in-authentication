from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
  Emp_no=models.CharField(max_length=5, primary_key=True)
  Emp_name = models.CharField(max_length = 50, blank = True, null = True, unique = True)
  Department=models.CharField(max_length=40)
  email = models.EmailField( unique = True)
  profile_pic=models.ImageField()
  username=None
  password=models.CharField(max_length=255)
  
  # email field is used for login purpose instead of username
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  # base64 for profile image
  @property 
  def image_url( self ):
        try:
            img = open( self.profile_pic.path, "rb") 
            data = img.read() 
            return "data:image/jpg;base64,%s" % data.encode('base64') 
 
        except IOError:
            return self.profile_pic.url

# model for nested serializer implementation
class Employeesalarydetail(models.Model):
    Emp_no=models.ForeignKey(Employee,related_name='salary',on_delete=models.CASCADE)
    Salary=models.CharField(max_length=20)
    Designation=models.CharField(max_length=30)

    class Meta:
        ordering = ('Emp_no',)
  

