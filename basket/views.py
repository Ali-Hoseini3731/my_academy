from django.shortcuts import render
from django.http import HttpResponse


def add_to_basket(request):
    return HttpResponse("Hello, world. You're at the add_to_basket view")
