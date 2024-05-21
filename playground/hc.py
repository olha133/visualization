import random
import numpy as np
import time
import pandas as pd
import os
import glob
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

class HillClimbingTSP:
    def __init__(self, num_cities=5, csv_file=None):
        self.num_cities = num_cities
        self.csv_file = csv_file
        self.positions, self.distance_matrix = self.generate_distance_matrix()
        self.random_seed = int(time.time())
        random.seed(self.random_seed)
        self.plot_counter = 0

    def generate_distance_matrix(self):
        # If CSV file exists, read it. Otherwise, generate random positions and calculate the distance matrix
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
        for i in range(1, len(tour) - 2):  # Exclude the first and last city
            new_tour = tour[:]
            new_tour[i], new_tour[i + 1] = new_tour[i + 1], new_tour[i]  # Swap two adjacent cities
            neighbors.append(new_tour)
        return neighbors
    
    def plot_graph_step(self, G, positions, tour=None, swapped_edges=None, swapped_nodes=None):
        plt.clf()
        pos = {i: (positions[i][0], positions[i][1]) for i in range(len(positions))}
        
        if tour:
            path_edges = list(zip(tour, tour[1:]))
        path_edges_background = list(G.edges)
        nx.draw(G, pos, with_labels=False, edgelist=path_edges_background, edge_color='#dbdbdb', width=1.5)
        labels = {i: i + 1 for i in G.nodes()}
        nx.draw(G, pos, labels=labels, node_color='#65B48E', node_size=350, font_size=10, edgelist=path_edges, edge_color='#3E5CC5', width=2)

        if swapped_edges:
            nx.draw_networkx_edges(G, pos, edgelist=swapped_edges, edge_color='#E64E00', width=2)
        
        if swapped_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=swapped_nodes, node_color='#E6EB00', node_size=350)
        
        # Save the plot
        plot_filename = f'plots/plot_{self.plot_counter}.png'
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
    
    def run(self):
        # Generate a random initial tour
        tour = list(range(self.num_cities))
        random.shuffle(tour)
        tour.append(tour[0])
        # Create a graph and visualize it
        G = self.generate_complete_graph()
        positions = {i: pos for i, pos in enumerate(self.positions)}
               
        self.plot_graph_step(G, positions, tour)

        while True:
            neighbors = self.get_neighbors(tour)
            current_distance = self.total_distance(tour)
            neighbors_distances = [self.total_distance(neighbor) for neighbor in neighbors]

            # If there's no improvement, break the loop
            if min(neighbors_distances) >= current_distance:
                break
            # Store the current tour before making a swap
            old_tour = tour[:]

            # Choose the neighbor with the smallest distance as the new tour
            tour = neighbors[np.argmin(neighbors_distances)]
             # Find the swapped cities
            swapped_edges = []
            swapped_nodes = []
            for i in range(len(tour) - 1):
                if old_tour[i] != tour[i]:
                    swapped_edges = [(tour[i-1], tour[i]), (tour[i+1], tour[i + 2])]
                    swapped_nodes = [tour[i-1], tour[i], tour[i+1], tour[i+2]]
                    break
         
            self.plot_graph_step(G, positions, tour, swapped_edges=swapped_edges, swapped_nodes=swapped_nodes)
            self.plot_graph_step(G, positions, tour)

        self.plot_graph_step(G, positions, tour)
        return tour, self.total_distance(tour)


def main():
    num_cities = 5
    files = glob.glob('plots/*')
    for f in files:
        os.remove(f)
    tsp = HillClimbingTSP(num_cities, r'C:\Users\Olha\study\Bachalor\code\my code\tour15.csv')
    best_tour, best_distance = tsp.run()
    print(f"Best tour: {best_tour}")
    print(f"Best distance: {best_distance}")


if __name__ == "__main__":
    main()