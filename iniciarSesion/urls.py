from django.urls import path
from .views import login_view,test_password_hashing

urlpatterns = [
    path('login/', login_view, name='login'),
    
    
]
