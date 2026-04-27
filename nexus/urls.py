"""
URL configuration for nexus project.

"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from nexusApp.admin_site import nexus_admin 
import nexusApp.admin   

urlpatterns = [
    path('admin/', nexus_admin.urls),  
    path('', include(('nexusApp.urls'))),
    path("accounts/",  include("django.contrib.auth.urls")),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)