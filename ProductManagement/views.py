from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from ProductManagement.models import Category, Product
from ReviewManagement.models import Review
from UserManagement.models import Consumer

from .fetchamazonreviews import fetch_amazon_reviews
# Create your views here.
def product(request):
    product = Product.objects.filter(title=request.POST.get("product_title"))[0]
    ccreviews = Review.objects.filter(product=product)
    if request.user.is_authenticated:
        if len(Review.objects.filter(product=product,consumer=Consumer.objects.filter(username=request.user.username)[0]))==0:
            return render(request, 'product.html',{'product':product,'ccreviews':ccreviews,'username':request.user.username,"writereview":True,"consumer":Consumer.objects.get(username=request.user.username),"categories":Category.objects.all()})
        return render(request, 'product.html',{'product':product,'ccreviews':ccreviews,'username':request.user.username,"writereview":False,"consumer":Consumer.objects.get(username=request.user.username),"categories":Category.objects.all()})
    return render(request, 'product.html',{'product':product,'ccreviews':ccreviews,'username':request.user.username,"writereview":False,"categories":Category.objects.all()})
html_email_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Added Confirmation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background-color: #1e90ff;
            padding: 20px;
            text-align: center;
            border-radius: 8px 8px 0 0;
            color: #ffffff;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .email-body {{
            padding: 20px;
            line-height: 1.6;
        }}
        .email-body h2 {{
            font-size: 20px;
            color: #1e90ff;
        }}
        .email-body p {{
            font-size: 16px;
            color: #555;
        }}
        .button {{
            display: inline-block;
            padding: 12px 20px;
            background-color: #1e90ff;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            color: #aaa;
            font-size: 12px;
        }}
        .footer a {{
            color: #1e90ff;
            text-decoration: none;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Email Header -->
        <div class="header">
            <h1>Thank You for Adding a New Product!</h1>
        </div>
        <!-- Email Body -->
        <div class="email-body">
            <h2>Hello {user_name},</h2>
            <p>
                We're excited to let you know that your product <strong>{product_name}</strong> has been successfully added to our website, <strong>Consumer Compass</strong>.
            </p>
            <p>
                Thank you for contributing to our growing community of users. Your product will now be visible to our visitors who are searching for reliable reviews and product information.
            </p>

            <p>
                We appreciate your support, and we look forward to seeing more great contributions from you!
            </p>
            <p>
                Best regards,<br>
                The Consumer Compass Team
            </p>
        </div>
        <!-- Email Footer -->
        <div class="footer">
            <p>
                If you have any questions or need assistance, feel free to <a href="/contact">contact us</a>.
            </p>
            <p>&copy; 2024 Consumer Compass. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

# Formatting the template with actual values



def addproduct(request):
    context = {
        "categories":Category.objects.all()
    }
    if request.user.is_authenticated:
        context["consumer"]=Consumer.objects.get(username=request.user.username)
    if request.method == 'POST':
        reviews = fetch_amazon_reviews(request.POST.get("amazon_link"), 1)
        half = len(reviews) // 2  # Integer division to get the midpoint
        amazonreviews = reviews[:half]  # First half
        flipkartreviews = reviews[half:]  # Second half

        product = Product(title=request.POST.get("title"),category=Category.objects.get(name=request.POST.get("category")),ccscore=0,amazonreviews=amazonreviews,image=request.FILES['image'],flipkartreviews=flipkartreviews,online_rating=0,price=request.POST.get("price"))
        product.save()
        context["redirect"] = True
        context["product_title"] = product.title
        # Properly formatted email template
        try:
            formatted_email = html_email_template.format(
                user_name=request.user.username,
                product_name=product.title,
            )

            # Creating the email message
            email_message = EmailMessage(
                "Thanks for Adding a Product on Consumer Compass",  # subject of the email
                formatted_email,  # HTML email body
                "ConsumerCompassHelp@gmail.com",  # from email
                [request.user.email]  # recipient list (should be a list)
            )

            # Setting the content type to HTML
            email_message.content_subtype = "html"

            # Sending the email
            email_message.send(fail_silently=False)
        except:
            print("Email sending failed!")

        return  render(request, 'addproduct.html',context)
    context["redirect"] = False
    return render(request, 'addproduct.html',context)