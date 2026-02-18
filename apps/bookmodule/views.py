from django.shortcuts import render
from django.http import HttpResponse
'''
#task1
def index(request):
    return HttpResponse("Hello, world!")

#task2
def index(request):
    name = request.GET.get("name") or "world!"
    return HttpResponse("Hello, " + name) #http://127.0.0.1:8000?name=Mousa
 '''
 #task3
def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1)) #http://127.0.0.1:8000/index2/10/
'''
#task4
def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html")
'''
#task5
def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})


def viewbook(request, bookId):
    book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
    book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}

    targetBook = None
    if book1['id'] == bookId:
        targetBook = book1
    if book2['id'] == bookId:
        targetBook = book2

    context = {'book': targetBook}
    return render(request, 'bookmodule/show.html', context)
