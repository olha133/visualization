from django.shortcuts import render
# Create your views here.

algorithms = [
    {"key": "hc", "name": "Hill climber"},
    {"key": "hc_restarts", "name" : "Hill climber with restarts"},
    {"key": "hc_larger_radii", "name" : "Hill climber with larger search radii"}
]

def hc(request):
    return render(request, "playground/hc.html", {"algorithms": algorithms})

def hc_restarts(request):
    return render(request, "playground/hc_restarts.html")

def hc_larger_radii(request):
    return render(request, "playground/hc_larger_radii.html")