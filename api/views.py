from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from .serializers import MainModelSerializer, BoostSerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def index(request):
   user = User.objects.filter(id=request.user.id).first()
   if user == None:
      return redirect('login')
   mainmodel = models.MainModel.objects.filter(user=request.user).first()
   boosts = mainmodel.boost_set.all()

   return render(request, 'index.html', {
       'mainmodel': mainmodel,
       'boosts': boosts
   })

@api_view(['GET'])
def call_click(request):
    mainmodel = models.MainModel.objects.filter(user=request.user).first()
    mainmodel.click()

    boosts=None
    is_level_up = mainmodel.is_level_up()

    mainmodel.save()
    if is_level_up == 1:
        boost = models.Boost(mainModel=mainmodel, power=mainmodel.level*20, price=mainmodel.level*50)
        boost.save()

        boosts = [BoostSerializer(boost).data for boost in mainmodel.boost_set.all()]
    elif is_level_up == 2:
        boost = models.Boost(mainModel=mainmodel, power=mainmodel.level*10, price=mainmodel.level*100, boost_type=1)
        boost.save()

        boosts = [BoostSerializer(boost).data for boost in mainmodel.boost_set.all()]
    return Response({
        'mainmodel': MainModelSerializer(mainmodel).data,
        'boosts': boosts
    })

def register(request):
   if request.method == 'POST':
      form = UserCreationForm(request.POST)

      if form.is_valid():
         user = form.save()

         mainmodel = models.MainModel()
         mainmodel.user = user
         mainmodel.save()

         boost = models.Boost(mainModel = mainmodel)
         boost.save()

         return redirect('login')
      else:
         return render(request, 'registration/register.html', {'form': form})

   form = UserCreationForm()
   return render(request, 'registration/register.html', {'form': form})

@api_view(['POST'])
def buy_boost(request):
    boost_id = request.data['boost_id']

    boost = models.Boost.objects.get(id=boost_id)
    mainmodel = boost.update()
    boost.save()

    boosts = [BoostSerializer(boost).data for boost in mainmodel.boost_set.all()]

    return Response({
        'mainmodel': MainModelSerializer(mainmodel).data,
        'boosts': boosts
    })

def leaders(request):
    users = User.objects.all()
    leaders_dict = {}
    for i in users:
        model = models.MainModel.objects.filter(user=i).first()
        leaders_dict[model.click_count] = i.username

    sorted_dict = {}
    for k in sorted(leaders_dict.keys(), reverse=True):
        sorted_dict[k] = leaders_dict[k]

    return render(request, 'leaders.html', {'leaders': sorted_dict.values(), 'values': sorted_dict.keys()})

def stats(request):
    model = models.MainModel.objects.filter(user=request.user).first()
    len_boosts = len([BoostSerializer(boost).data for boost in model.boost_set.all()])
    return render(request, 'stats.html', {
        'lenBoosts': len_boosts,
        'clickCount': model.click_count,
        'clickPower': model.click_power,
        'autoClickPower': model.auto_click_power,
        'level': model.level
    })
