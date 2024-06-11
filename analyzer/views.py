from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home (request):
    #return HttpResponse('Hello world') return file .html
    return render(request, 'hello.html', {'name': 'Rick'})
