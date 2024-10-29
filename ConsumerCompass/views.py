


from django.shortcuts import render

from ProductManagement.models import Category
from UserManagement.models import Consumer
def welcomepage(request):
    cats = Category.objects.all()
    context  ={
        "cats":cats
    }
    if request.user.is_authenticated:
        context["username"] = request.user.username
    return render(request,"welcome.html",context)

def aboutus(request):
    if request.user.is_authenticated:
        return render(request,"about.html",{"consumer":Consumer.objects.get(username=request.user.username),"categories":Category.objects.all()})
    return render(request,"about.html",{"categories":Category.objects.all()})

