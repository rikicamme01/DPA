#mapp urls to views model
from django.urls import path
from . import views

#urlconf
# all the added path contain implicitly the previous analyzer/... 
urlpatterns = [
    path('hello/', views.home)


]