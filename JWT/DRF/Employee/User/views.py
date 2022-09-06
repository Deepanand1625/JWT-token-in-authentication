from logging import raiseExceptions
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import EmployeeSerializer,EmployeedetailSerializer
from rest_framework.response import Response
from .models import Employee, Employeesalarydetail
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.shortcuts import get_object_or_404

class Registerview(APIView):
  def post(self, request):
    serializer=EmployeeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

class Loginview(APIView):
  def post(self, request):
    email=request.data['email']
    password=request.data['password']
    user=Employee.objects.filter(email=email).first()

    if user is None:
      raise AuthenticationFailed("User is not found")

    if not user.check_password(password):
       raise AuthenticationFailed("Incorrect Password")

    payload = {
            'Emp_no':user.Emp_no,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

    token = jwt.encode(payload, 'secret', algorithm='HS256')#.decode('utf-8')
    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
            'jwt': token
        }
    return response

class Userview(APIView):
  def get(self, request):
    token=request.COOKIES.get('jwt')
    if not token:
            raise AuthenticationFailed('Unauthenticated!')

    try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

    user = Employee.objects.filter(Emp_no=payload['Emp_no']).first()
    serializer = EmployeeSerializer(user)
    return Response(serializer.data)


class Logoutview(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

# CRUD operations on employee data
class CRUDoperations(APIView):
    def get(self, request, format=None, Emp_no=None):

       if Emp_no:
            emp = Employee.objects.get(Emp_no=Emp_no)
            serializer = EmployeeSerializer(emp)
            return Response(serializer.data)
       else:
            employee = Employee.objects.all()
            serializer = EmployeeSerializer(employee,many=True)
            return Response(serializer.data)
 
    def post(self, request, format=None):
        data = request.data
        serializer = EmployeeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()

        response.data = {
            'data': serializer.data,
            'message': 'New Employee data Created Successfully'
           
        }

        return response

    def put(self, request, Emp_no=None, format=None):
        emp= Employee.objects.get(Emp_no=Emp_no)
        serializer = EmployeeSerializer(instance=emp,data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        response = Response()

        response.data = {
            'message': 'Employee details Updated Successfully',
            'data': serializer.data
        }

        return response

    def delete(self, request, Emp_no, format=None):
        emp= get_object_or_404(Employee, Emp_no=Emp_no)
        emp.delete()
        return Response({
            'message': 'Employee Deleted Successfully'
        })


# Response we can get, has nested serializer format
class Employeesalaryview(APIView):
     def get(self,request, format=None):
           employee = Employeesalarydetail.objects.all()
           serializer =EmployeedetailSerializer(employee,many=True)
           return Response(serializer.data)
           
     def post(self, request, format=None, Emp_no=None):
        emp=Employee.objects.get(Emp_no=Emp_no)
        data = request.data
        serializer = EmployeedetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(Emp_no=emp)
        response = Response()

        response.data = {
            'data': serializer.data,
            'message': 'Employee salary data Created Successfully'
           
        }

        return response

   
    


     