from django.shortcuts import redirect, render
from django.http import HttpResponse 
from .models import expedition
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView
from django.urls import reverse_lazy
from .forms import ExpeditionForm


# Create your views here.
def home(request):
    return HttpResponse("<h1>welcome to the Expeditions App</h1>")
def welcome(request,name):
    return HttpResponse(f"<h1>Welcome {name} to the Expeditions App</h1>")
def listExpeditions(request):
    list=expedition.objects.filter(statut='publiee')
    return render(request,'expedition/list.html',{"liste":list})
def detailExpedition(request,pk):
    exp=expedition.objects.get(pk=pk)
    return render(request,'expedition/detail.html',{"exp":exp})    
    # delete sans render
def deleteExpedition(request,pk):
    exp=expedition.objects.get(pk=pk)
    exp.delete()
    return redirect('list')
class Expedition_list(ListView):
    model=expedition
    template_name='expedition/list.html'
    context_object_name='liste'
class Expedition_detail(DetailView):
    model=expedition
    template_name='expedition/detail.html'
    context_object_name='exp'
class Expedition_delete(DeleteView):
    model=expedition
    template_name='expedition/expedition_confirm_delete.html'
    success_url=reverse_lazy('expedition_list')
class Expedition_create(CreateView):
    model=expedition
    # fields=['ville_depart','ville_arrivee','poids_kg','date_souhaitee','description','entreprise']
    template_name='expedition/forms.html'
    success_url=reverse_lazy('expedition_list')
    form_class=ExpeditionForm
class Expedition_update(UpdateView):
    model=expedition
    template_name='expedition/forms.html'
    success_url=reverse_lazy('expedition_list')
    form_class=ExpeditionForm    