from django.http import HttpResponse


def products_list(request):
    return HttpResponse("products list page")
