from django.shortcuts import render
from .hc import HillClimbing
from .hc_restarts import HillClimbingRestarts
import os
import random
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import re
import csv
# Create your views here.

# Sorting function
def extract_number(string):
    match = re.search(r'plot_(\d+).png', string)
    return int(match.group(1)) if match else -1

def validate_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        if len(rows) < 4:
            return False, "The file must have at least 4 rows."
        if len(rows[0]) != 2:
            return False, "The file must have exactly 2 columns for X and Y coordinates."
    return True, None

def hc(request):
    if request.method == 'POST':
        if 'custom_file' in request.FILES:
            uploaded_file = request.FILES['custom_file']
            filepath = os.path.join(settings.BASE_DIR, 'data', 'custom_maps', uploaded_file.name)
            with open(filepath, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            is_valid, error_message = validate_csv(filepath)
            if not is_valid:
                return JsonResponse({'error': error_message}, status=400)
        else:
            num_cities = int(request.POST.get('city_count'))
            filename = f'tour{num_cities}.csv'
            filepath = os.path.join(settings.BASE_DIR, 'data', 'defined_maps', filename)
        # print(filepath)
        context = dict()
            
        # Clean up old plot files
        plots_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
        for file in os.listdir(plots_dir):
            file_path = os.path.join(plots_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
                
        hc = HillClimbing(csv_file = filepath)
        tour, distance = hc.run()

        # Gather plot file paths
        plot_files = [
            os.path.join(settings.MEDIA_URL, 'plots', file).replace('\\', '/')
            for file in os.listdir(plots_dir)
            if file.endswith('.png')
        ]
        plot_files = sorted(plot_files, key=extract_number)
        # print(type(plot_files))

        context.update({
            'tour': tour,
            'distance': distance,
            'plot_files': plot_files
        })
        # print(context['plot_files'])
        return JsonResponse(context)
    else:
        return render(request, 'playground/hc.html')


def hc_restarts(request):
    if request.method == 'POST':
        if 'custom_file' in request.FILES:
            uploaded_file = request.FILES['custom_file']
            filepath = os.path.join(settings.BASE_DIR, 'data', 'custom_maps', uploaded_file.name)
            with open(filepath, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            is_valid, error_message = validate_csv(filepath)
            if not is_valid:
                return JsonResponse({'error': error_message}, status=400)
        else:
            num_cities = int(request.POST.get('city_count'))
            filename = f'tour{num_cities}.csv'
            filepath = os.path.join(settings.BASE_DIR, 'data', 'defined_maps', filename)
        # print(filepath)
        context = dict()
        iterations = int(request.POST.get('iterations', 1)) # Get the number of iterations

        # Clean up old plot files
        plots_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
        for file in os.listdir(plots_dir):
            file_path = os.path.join(plots_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
                
        hc = HillClimbingRestarts(num_runs = iterations, csv_file = filepath)
        tour, distance = hc.run()

        # Gather plot file paths
        plot_files = [
            os.path.join(settings.MEDIA_URL, 'plots', file).replace('\\', '/')
            for file in os.listdir(plots_dir)
            if file.endswith('.png')
        ]
        plot_files = sorted(plot_files, key=extract_number)
        # print(type(plot_files))

        context.update({
            'tour': tour,
            'distance': distance,
            'plot_files': plot_files
        })
        # print(context['plot_files'])
        return JsonResponse(context)
    else:
        return render(request, 'playground/hc_restarts.html')

def hc_larger_radii(request):
    return render(request, "playground/hc_larger_radii.html")

