from django.shortcuts import render
from django.http import HttpResponseNotFound
from django import forms
import random
import markdown2


from . import util

class NewTaskForm(forms.Form):
    new_title = forms.CharField(label="Title of New Page", initial='Title...')
    new_page = forms.CharField(label="Type New Page", widget=forms.Textarea)

    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

def entry(request, title):
    if util.get_entry(title) != None:
        return render(request, "wiki/title.html", {
            "entry": util.get_entry(title),
            "title": title
        })
    else:
        return HttpResponseNotFound('<h1>Entry not exist</h1>')

def search(request):
    if request.method == "POST":
        temp_dict = request.POST
        query = temp_dict["q"]
        answ = util.search_entries(query)
        if answ != None:
            return render(request, "wiki/title.html", {
            "entry": util.get_entry(answ),
            "title": answ
            })
        else:
            return render(request, "encyclopedia/list_of_search.html", {
                "entries": util.search_sim_entries(query)
            })

def new(request):
    
    if request.method == "POST":
        page = NewTaskForm(request.POST)
        if page.is_valid():
            title = page.cleaned_data["new_title"]
            texts = page.cleaned_data["new_page"]
            saved = util.save_entry(title, texts)
            if saved:
                return render(request, "wiki/title.html", {
                    "entry": texts,
                    "title": title
                })
            elif saved == False:
                alert = True
                return render(request, "wiki/new.html", {
                    "form": NewTaskForm(),
                    "alert": alert
                })       
    return render(request, "wiki/new.html", {
        "form": NewTaskForm()
    })

def edit(request, title):
    if request.method == "POST":
        page = NewTaskForm(request.POST)
        if page.is_valid():
            title = page.cleaned_data["new_title"]
            texts = page.cleaned_data["new_page"]
            saved = util.edit_entry(title, texts)
            if saved:
                return render(request, "wiki/title.html", {
                    "entry": texts,
                    "title": title
                })
            else:
                alert = True
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries(),
                    "alert": alert
                    })


    if util.get_entry(title) != None:
        content = util.get_entry(title)
        initial_dict = {
            "new_title": title,
            "new_page": content,
        }
        return render(request, "wiki/edit.html", {
            "form": NewTaskForm(request.POST or None, initial = initial_dict),
            "title": title
        })

def random_page(request):
    entries = util.list_entries()
    num = random.randint(0, len(entries))
    title = entries[num]
    return render(request, "wiki/title.html", {
        "entry": util.get_entry(title),
        "title": title
    })
