"""
URL configuration for ConsumerCompass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ConsumerCompass import settings
from django.conf.urls.static import static
from .views import welcomepage,aboutus
from UserManagement.views import home,register,login_view,logout_view
from ProductManagement.views import product,addproduct
from ReviewManagement.views import writereview,editreview,changeapproval

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", welcomepage, name="welcome"),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('editreview/', editreview, name='editreview'),
    path('addproduct/', addproduct, name='addproduct'),
    path('product/', product, name='product'),
    path('aboutus/', aboutus, name='aboutus'),
    path('changeapproval/', changeapproval, name='changeapproval'),
    path('writereview/<str:producttitle>', writereview, name='writereview'),
    path('<str:cat>/', home, name='home'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)