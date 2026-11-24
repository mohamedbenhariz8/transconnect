from django.shortcuts import render
from .models import Entreprise
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView
from django.urls import reverse_lazy
from .forms import EntrepriseForm,InscriptionForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class entreprises_list(ListView):
    model = Entreprise
    template_name = 'entreprise/entreprises_list.html'
    context_object_name = 'entreprises'
class entreprises_detail(DetailView):
    model = Entreprise
    template_name = 'entreprise/entreprises_detail.html'
    context_object_name = 'entreprise'
class entreprises_delete(DeleteView):
    model = Entreprise
    template_name = 'entreprise/entreprises_confirm_delete.html'
    success_url = reverse_lazy('entreprises_list')
class entreprises_create(CreateView):
    model = Entreprise
    template_name = 'entreprise/entreprises_form.html'
    success_url = reverse_lazy('entreprises_list')
    form_class = EntrepriseForm
class entreprises_update(UpdateView):
    model = Entreprise
    template_name = 'entreprise/entreprises_form.html'
    success_url = reverse_lazy('entreprises_list')
    form_class = EntrepriseForm
def inscriptionView(request):
    if request.method == 'POST' :
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
    else :
        form = InscriptionForm()

    return render(request, 'inscription.html', {'form': form})
    


    
