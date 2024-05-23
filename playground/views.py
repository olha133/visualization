from django.shortcuts import render
from .hc import HillClimbing
import os
import random
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.

def hc(request):
    context = dict()
        
    # Clean up old plot files
    plots_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
    # for file in os.listdir(plots_dir):
    #     file_path = os.path.join(plots_dir, file)
    #     if os.path.isfile(file_path):
    #         os.unlink(file_path)
            
    # num_cities = random.randint(5, 20)
    # hc = HillClimbing(num_cities)
    # tour, distance = hc.run()
    tour = [1,2,3,4]
    distance = 0.5

    # Gather plot file paths
    plot_files = sorted([
        os.path.join(settings.MEDIA_URL, 'plots', file).replace('\\', '/')
        for file in os.listdir(plots_dir)
        if file.endswith('.png')
    ])

    context.update({
        'tour': tour,
        'distance': distance,
        'plot_files': plot_files
    })
    # print(context['plot_files'])

    return render(request, 'playground/hc.html', context)
# def hc(request):
#     return render(request, "playground/hc.html", {"algorithms": algorithms})

def hc_restarts(request):
    return render(request, "playground/hc_restarts.html")

def hc_larger_radii(request):
    return render(request, "playground/hc_larger_radii.html")

