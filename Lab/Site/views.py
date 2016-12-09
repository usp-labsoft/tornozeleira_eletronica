from django.shortcuts import render, get_object_or_404
from .models import Pessoa

def pessoas_list(request):
    pessoas = Pessoa.objects.order_by('first_name')
    return render(request, 'Site/pessoas_list.html', {'pessoas' : pessoas})

def pessoa_local(request, pk):
    pessoa = get_object_or_404(Pessoa, pk = pk)
    return render(request, 'Site/pessoa_local.html', {'pessoa' : pessoa})
