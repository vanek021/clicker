from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models

# Create your views here.
def index(request):
   mainmodel = models.MainModel.objects.first()
   return render(request, 'index.html', {'mainmodel': mainmodel})

@api_view(['GET'])
def call_click(request):
   mainmodel = models.MainModel.objects.first()
   mainmodel.click()
   mainmodel.save()
   #return Response(mainmodel.click_count)
   return render(request, 'index.html', {'mainmodel': mainmodel})