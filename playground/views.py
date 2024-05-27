from django.shortcuts import render
from .hc import HillClimbing
from .hc_restarts import HillClimbingRestarts
from .hc_larger_radii import HillClimbingLargerRadii
import os
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
        if len(rows) < 5:
            return False, "The file must have at least 5 rows."
        if len(rows[0]) != 2:
            return False, "The file must have exactly 2 columns for X and Y coordinates."
    return True, None

def handle_file_upload(request):
    if 'custom_file' in request.FILES:
        uploaded_file = request.FILES['custom_file']
        filepath = os.path.join(settings.BASE_DIR, 'data', 'custom_maps', uploaded_file.name)
        with open(filepath, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        is_valid, error_message = validate_csv(filepath)
        if not is_valid:
            return None, error_message
    else:
        num_cities = int(request.POST.get('city_count'))
        filename = f'tour{num_cities}.csv'
        filepath = os.path.join(settings.BASE_DIR, 'data', 'defined_maps', filename)
    return filepath, None

def cleanup_old_plots():
    plots_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
    for file in os.listdir(plots_dir):
        file_path = os.path.join(plots_dir, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

def get_plot_files():
    plots_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
    plot_files = [
        os.path.join(settings.MEDIA_URL, 'plots', file).replace('\\', '/')
        for file in os.listdir(plots_dir)
        if file.endswith('.png')
    ]
    return sorted(plot_files, key=extract_number)

def run_algorithm(algorithm_class, request):
    filepath, error_message = handle_file_upload(request)
    if error_message:
        return JsonResponse({'error': error_message}, status=400)
    
    cleanup_old_plots()
    if algorithm_class == HillClimbingRestarts:
        iterations = int(request.POST.get('iterations', 1))
        algorithm = algorithm_class(csv_file=filepath, num_runs=iterations)
    else:
        algorithm = algorithm_class(csv_file=filepath)
    tours, swapped_nodes_list, distances, elapsed_time = algorithm.run()
    plot_files = get_plot_files()
    
    return JsonResponse({
        'tours': tours,
        'swapped_nodes_list': swapped_nodes_list,
        'distances': distances,
        'plot_files': plot_files,
        'elapsed_time': elapsed_time
    })

def hc(request):
    if request.method == 'POST':
        return run_algorithm(HillClimbing, request)
    else:
        return render(request, 'playground/hc.html')

def hc_restarts(request):
    if request.method == 'POST':
        return run_algorithm(HillClimbingRestarts, request)
    else:
        return render(request, 'playground/hc_restarts.html')

def hc_larger_radii(request):
    if request.method == 'POST':
        return run_algorithm(HillClimbingLargerRadii, request)
    else:
        return render(request, 'playground/hc_larger_radii.html')