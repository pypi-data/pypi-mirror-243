from django.urls import path
from django.http import HttpRequest
from django.shortcuts import render

from core.forms import DemoWidgetsForm


def index(request: HttpRequest) -> str:
    if request.method == "POST":
        print(f'{request.POST=}')
        form = DemoWidgetsForm(request.POST)
        if form.is_valid():
            context = {"form": form, "result": form.cleaned_data}
        else:
            context = {"form": form}
    else:
        form = DemoWidgetsForm()
        context = {"form": form}
    return render(request, "index.html", context)


urlpatterns = [
    path("", index),
]
