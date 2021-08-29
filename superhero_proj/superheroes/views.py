from typing import ContextManager
from django.db.models import fields
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Superhero
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from .forms import SuperheroForm

# Create your views here.
def edit(request, hero_id):
    context = {}
    single_hero = Superhero.objects.get(pk=hero_id)
    form = SuperheroForm(request.POST or None, instance=single_hero)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('superheroes:index'))
    context["form"] = form

    return render(request, 'superheroes/edit.html', context)

def index(request):
    all_heroes = Superhero.objects.all()
    context = {
        'all_heroes': all_heroes
    }
    return render(request, 'superheroes/index.html', context)

def detail(request, hero_id):
    single_hero = Superhero.objects.get(pk=hero_id) #might get an exception if multiple objects, good place for a try catch
    context = {
        'single_hero': single_hero
    }
    return render(request, 'superheroes/detail.html', context)

def create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        alter_ego = request.POST.get('alter_ego')
        primary = request.POST.get('primary')
        secondary = request.POST.get('secondary')
        catch_phrase = request.POST.get('catchphrase')
        new_hero = Superhero(name=name, alter_ego=alter_ego, primary_ability=primary, secondary_ability=secondary, catch_phrase=catch_phrase)
        new_hero.save()
        return HttpResponseRedirect(reverse('superheroes:index'))
    else:
        return render(request, 'superheroes/create.html')

def delete(request, hero_id):
    single_hero = Superhero.objects.get(pk=hero_id)
    context = {
        'single_hero': single_hero
    }
    if request.method == "POST":
        single_hero.delete()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'superheroes/delete.html')


