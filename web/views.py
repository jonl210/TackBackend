from django.shortcuts import render

#Render home page
def index(request):
    return render(request, "web/index.html")

#Render terms page
def terms(request):
    return render(request, "web/terms.html")

#Render privacy page
def privacy(request):
    return render(request, "web/privacy.html")
