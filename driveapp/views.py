from django.shortcuts import render

# Create your views here.
def car(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_1.html', context)

def car2(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_2.html', context)

def manage_login(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_login.html', context)
def manage_menu(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_menu.html', context)

def manage_menuadd(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_menu_add.html', context)