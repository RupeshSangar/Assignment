from django.shortcuts import render
import pandas as pd
from ..serializers import *
from ..models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage


# Create your views here.
    

def home(request):
    if request.method == 'POST':
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename) 
        df = pd.read_csv(filename)
        
        for dbframe in df.itertuples():
            obj = EmployeeDetails.objects.create(first_name=dbframe.first_name,last_name = dbframe.last_name,email=dbframe.email)           
            obj.save()
        Employee_data = EmployeeDetails.objects.all().values()
        return render(request, 'index.html', context = {'uploaded_file_url': uploaded_file_url,"data":Employee_data})
    # Employee_data = Employee.objects.all().values()   
    return render(request, 'index.html')
    

class UploadFile(APIView):

    def get(self,request):
        emp_data = EmployeeDetails.objects.all()
        serializer = EmployeeSerializer(emp_data, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        else:
            return Response(serializer.errors, status = 400)
        


class SortedDataView(APIView):
    def get(self,request):
        queryset = EmployeeDetails.objects.all().order_by('first_name')[:50]
        serializer = EmployeeSerializer(queryset, many=True)

        return Response(serializer.data)