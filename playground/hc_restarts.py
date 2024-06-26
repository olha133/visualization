from django.conf import settings
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import random
import numpy as np
import time
import pandas as pd
import os
import networkx as nx
import matplotlib
matplotlib.use('Agg')


class HillClimbingRestarts:
    def __init__(self, num_runs=1, csv_file=None, weighted=False):
        self.num_runs = num_runs
        self.csv_file = csv_file
        self.positions, self.distance_matrix = self.generate_distance_matrix()
        self.random_seed = int(time.time())
        random.seed(self.random_seed)
        self.plot_counter = 0
        self.weighted = weighted


    def generate_distance_matrix(self):
        # If CSV file exists, read it. Otherwise, generate random positions and calculate the distance matrix
        if self.csv_file and os.path.exists(self.csv_file):
            data = pd.read_csv(self.csv_file, header=0).values
            positions = data[:, :2]
            distance_matrix = squareform(pdist(positions, 'euclidean'))
            self.num_cities = len(distance_matrix)
        else:
            return None
        return positions, distance_matrix

    def total_distance(self, tour):
        return sum(self.distance_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1)) + self.distance_matrix[tour[-1], tour[0]]

    def get_neighbors(self, tour):
        neighbors = []
        for i in range(1, len(tour) - 2):  # Exclude the first and last city
            new_tour = tour[:]
            new_tour[i], new_tour[i + 1] = new_tour[i +
                                                    1], new_tour[i]  # Swap two adjacent cities
            neighbors.append(new_tour)
        return neighbors

    def plot_graph_step(self, G, positions, tour=None, edge_colors='#3E5CC5', node_colors='#65B48E', swapped_edges=None, swapped_nodes=None):
        plt.clf()
        pos = {i: (positions[i][0], positions[i][1])
               for i in range(len(positions))}

        if tour:
            path_edges = list(zip(tour, tour[1:]))
        path_edges_background = list(G.edges)
        nx.draw(G, pos, with_labels=False, edgelist=path_edges_background,
                edge_color='#dbdbdb', width=1.5)
        labels = {i: i + 1 for i in G.nodes()}
        nx.draw(G, pos, labels=labels, node_color=node_colors, node_size=350,
                font_size=10, edgelist=path_edges, edge_color=edge_colors, width=2)

        if swapped_edges:
            nx.draw_networkx_edges(
                G, pos, edgelist=swapped_edges, edge_color='#E64E00', width=2)

        if swapped_nodes:
            nx.draw_networkx_nodes(
                G, pos, nodelist=swapped_nodes, node_color='#E6EB00', node_size=350)
            
        if self.weighted and tour:
            edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in path_edges}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color=edge_colors)
            
            # Save the plot
        plot_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)
        plot_filename = os.path.join(plot_dir, f'plot_{self.plot_counter}.png')
        plt.savefig(plot_filename, dpi=500)

        self.plot_counter += 1

    def generate_complete_graph(self):
        G = nx.Graph()
        n = len(self.distance_matrix)
        for i in range(n):
            for j in range(i + 1, n):  # Only add one direction for symmetric TSP
                if self.distance_matrix[i][j] != 0:
                    G.add_edge(i, j, weight=self.distance_matrix[i][j])
        return G

    def run(self, weighted=False):
        start_time = time.time()
        best_tour = None
        best_distance = float('inf')
        tours = []
        distances = []
        for _ in range(self.num_runs):
            # Generate a random initial tour
            tour = list(range(self.num_cities))
            random.shuffle(tour)
            tour.append(tour[0])
            # Create a graph and visualize it
            G = self.generate_complete_graph()
            positions = {i: pos for i, pos in enumerate(self.positions)}

            while True:
                neighbors = self.get_neighbors(tour)
                current_distance = self.total_distance(tour)
                neighbors_distances = [self.total_distance(
                    neighbor) for neighbor in neighbors]

                # If there's no improvement, break the loop
                if min(neighbors_distances) >= current_distance:
                    break
                # Store the current tour before making a swap
                old_tour = tour[:]

                # Choose the neighbor with the smallest distance as the new tour
                tour = neighbors[np.argmin(neighbors_distances)]

                for i in range(len(tour) - 1):
                    if old_tour[i] != tour[i]:
                        swapped_edges = [(tour[i-1], tour[i]),
                                         (tour[i+1], tour[i + 2])]
                        swapped_nodes = [tour[i-1],
                                         tour[i], tour[i+1], tour[i+2]]
                        break

            tour_distance = self.total_distance(tour)
            if tour_distance < best_distance:
                best_tour = tour
                best_distance = tour_distance

            tours.append([node + 1 for node in tour])
            distances.append(tour_distance)

            self.plot_graph_step(G, positions, tour)

        tours.append([node + 1 for node in best_tour])
        distances.append(best_distance)

        self.plot_graph_step(G, positions, best_tour,
                             edge_colors='#E64E00', node_colors='#f05100')

        end_time = time.time()  # End timing
        elapsed_time = end_time - start_time

        return tours, None, distances, elapsed_time
