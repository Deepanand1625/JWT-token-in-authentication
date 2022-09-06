from rest_framework import serializers
from User.models import Employee, Employeesalarydetail

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('Emp_no', 'Emp_name','email','profile_pic','Department','password',)
        extra_kwargs={
          "password":{'write_only':True}
        }

    def create(self, validated_data):
        password=validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
          instance.set_password(password)
        instance.save()
        return instance

# class EmployeesalarydetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employeesalarydetail
#         fields = ('Emp_no', 'Salary','Designation',)

#nested serializer implementation

class EmployeedetailSerializer(serializers.ModelSerializer):
  Employee=EmployeeSerializer(source='Emp_no', read_only=True)
      
  class Meta:
      model=Employeesalarydetail
      fields=('Employee','Salary','Designation')
      read_only_fields=('Employee',)
      