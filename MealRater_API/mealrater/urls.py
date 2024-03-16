
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('tokenrequest/',obtain_auth_token),          #we do this by defult to give to user in the system a token help them to get into the system  
]
