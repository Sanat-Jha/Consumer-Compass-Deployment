from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect, render

from ProductManagement.models import Category, Product
from ReviewManagement.models import Review
from UserManagement.models import Consumer

# Create your views here.
def writereview(request,producttitle):
    product = Product.objects.get(title=producttitle)
    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        review = request.POST.get("review")
        if len(Review.objects.filter(product=product,consumer=Consumer.objects.get(username=request.user.username))) == 0:
            review = Review(product=product, content=review,consumer=Consumer.objects.get(username=request.user.username))
            review.save()
            l = len(Review.objects.filter(product=product))
            product.ccscore = (product.ccscore*(l-1) + rating)/l
            product.save()
        if request.user.is_authenticated:
            return render(request, 'writereview.html',{'product':product, 'redirect':True,"consumer":Consumer.objects.get(username=request.user.username),"categories":Category.objects.all()})
        return render(request, 'writereview.html',{'product':product, 'redirect':True})
    if request.user.is_authenticated:
        return render(request, 'writereview.html',{'product':product, 'redirect':False,"consumer":Consumer.objects.get(username=request.user.username),"categories":Category.objects.all()})
    return render(request, 'writereview.html',{'product':product, 'redirect':False})


# @csrf_exempt
def editreview(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        product_title = data.get('product')
        new_content = data.get('content')

        # Find the review by username and product
        try:
            review = Review.objects.get(consumer__username=username, product__title=product_title)
            review.content = new_content
            review.save()

            # Return success response
            return JsonResponse({'success': True,'content':new_content,'username':username})

        except Review.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Review not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def changeapproval(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        reviewusername = data.get('reviewusername')
        print(username)
        product_title = data.get('product_title')
        print(product_title)
        approve = data.get('approve')
        print(approve)

        # Find the review by username and product
        
        review = Review.objects.get(consumer=Consumer.objects.get(username=reviewusername), product=Product.objects.get(title=product_title))
        review.toggle_approval(username)
        review.save()

        # Return success response
        return JsonResponse({'success': True,'approve':approve,'username':username, "approvescore":review.approvalscore})


    return JsonResponse({'success': False, 'error': 'Invalid request'})