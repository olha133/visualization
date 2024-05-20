# from django.shortcuts import render
# # Create your views here.

algorithms = [
    {"key": "hc", "name": "Hill climber"},
    {"key": "hc_restarts", "name" : "Hill climber with restarts"},
    {"key": "hc_larger_radii", "name" : "Hill climber with larger search radii"}
]

# def hc(request):
#     return render(request, "playground/hc.html", {"algorithms": algorithms})

# def hc_restarts(request):
#     return render(request, "playground/hc_restarts.html")

# def hc_larger_radii(request):
#     return render(request, "playground/hc_larger_radii.html")

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
import io
import urllib, base64
import random
import numpy as np
import pandas as pd
import os
import time
from scipy.spatial.distance import pdist, squareform

# Hill Climbing Algorithm Implementation
class HillClimbingTSP:
    def __init__(self, num_cities=5, csv_file=None):
        self.num_cities = num_cities
        self.csv_file = csv_file
        self.positions, self.distance_matrix = self.generate_distance_matrix()
        self.random_seed = int(time.time())
        random.seed(self.random_seed)

    def generate_distance_matrix(self):
        if self.csv_file and os.path.exists(self.csv_file):
            data = pd.read_csv(self.csv_file, header=None).values
            positions = data[:, :2]
            distance_matrix = squareform(pdist(positions, 'euclidean'))
            self.num_cities = len(distance_matrix)
        else:
            positions = np.random.rand(self.num_cities, 2)
            distance_matrix = squareform(pdist(positions, 'euclidean'))
        return positions, distance_matrix

    def total_distance(self, tour):
        return sum(self.distance_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1)) + self.distance_matrix[tour[-1], tour[0]]

    def get_neighbors(self, tour):
        neighbors = []
        for i in range(1, len(tour) - 2):
            new_tour = tour[:]
            new_tour[i], new_tour[i + 1] = new_tour[i + 1], new_tour[i]
            neighbors.append(new_tour)
        return neighbors

    def generate_complete_graph(self):
        G = nx.Graph()
        n = len(self.distance_matrix)
        for i in range(n):
            for j in range(i + 1, n):
                if self.distance_matrix[i][j] != 0:
                    G.add_edge(i, j, weight=self.distance_matrix[i][j])
        return G

    def run(self):
        tour = list(range(self.num_cities))
        random.shuffle(tour)
        tour.append(tour[0])
        while True:
            neighbors = self.get_neighbors(tour)
            current_distance = self.total_distance(tour)
            neighbors_distances = [self.total_distance(neighbor) for neighbor in neighbors]
            if min(neighbors_distances) >= current_distance:
                break
            tour = neighbors[np.argmin(neighbors_distances)]
        return tour, self.total_distance(tour)

def render_plot(tsp):
    fig, ax = plt.subplots(figsize=(8, 8))
    G = tsp.generate_complete_graph()
    positions = {i: (pos[0], pos[1]) for i, pos in enumerate(tsp.positions)}
    tour, _ = tsp.run()
    path_edges = list(zip(tour, tour[1:]))
    nx.draw(G, positions, with_labels=True, node_color='#65B48E', edge_color='#dbdbdb', node_size=500, ax=ax)
    nx.draw_networkx_edges(G, positions, edgelist=path_edges, edge_color='#E64E00', width=2, ax=ax)
    plt.title("TSP Visualization")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

def hc(request):
    tsp = HillClimbingTSP(num_cities=5)
    plot_url = render_plot(tsp)
    return render(request, "playground/hc.html", {"algorithms": algorithms, "plot_url": plot_url})

@csrf_exempt
def update_hc(request):
    num_cities = int(request.POST.get('num_cities', 5))
    tsp = HillClimbingTSP(num_cities=num_cities)
    plot_url = render_plot(tsp)
    return JsonResponse({"plot_url": plot_url})

def hc_restarts(request):
    return render(request, "playground/hc_restarts.html", {"algorithms": algorithms})

def hc_larger_radii(request):
    return render(request, "playground/hc_larger_radii.html", {"algorithms": algorithms})
