from django.shortcuts import render
from django.http import HttpResponseNotFound
from django import forms


from . import util

class NewPageForm(forms.Form):
    new_title = forms.CharField(label="Title of New Page")
    new_page = forms.CharField(label="Type New Page")
    


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
        page = NewPageForm(request.POST)
        title = page["new_title"]
        content = page["new_page"]
        util.save_entry(title, content)
    return render(request, "wiki/new.html", {
        "form": NewPageForm()
    })
