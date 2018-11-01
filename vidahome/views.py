from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    """A view of all bands."""
    return render(request, "home.html")
