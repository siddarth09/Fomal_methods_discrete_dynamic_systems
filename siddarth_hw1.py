import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


class Homework1():
    def __init__(self):
        # Creating variables for the class
        self.x = 0
        self.y = 0
        self.x_max = 10
        self.y_max = 8

    def get_grid(self, rows, cols):
        # Creating a grid with the given number of rows and columns
        if rows > self.x_max or cols > self.y_max:
            print("Grid size is too large")
            return None

        self.x = rows
        self.y = cols
        
    def prune_adjacency_matrix(self, adj_matrix, nodes, obstacles):
        # Getting indices of obstacles
        obstacle_indices = [nodes.index(node) for node in obstacles]
        adj_matrix = np.array(adj_matrix)
        
        for idx in obstacle_indices:
            adj_matrix[idx, :] = 0
            adj_matrix[:, idx] = 0
            
        return adj_matrix
    
    def create_graph(self, rows, cols, obstacles, rois, initial_state, final_state):
        # Creating nodes on grid
        self.get_grid(rows, cols)

        nodes = []
        for i in range(self.x):
            for j in range(self.y):
                nodes.append((i, j))

        g = nx.DiGraph()
        g.add_nodes_from(nodes)

        actions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1),
            'stay': (0, 0)
        }

        # Adding edges
        for node in nodes:
            if node in obstacles:
                continue 
            for action, (dx, dy) in actions.items():
                new_node = (node[0] + dx, node[1] + dy)
                if 0 <= new_node[0] < self.x and 0 <= new_node[1] < self.y and new_node not in obstacles:
                    g.add_edge(node, new_node, weight=1)
                
        adjacency_matrix = nx.adjacency_matrix(g).todense()
        pruned_adjacency_matrix = self.prune_adjacency_matrix(adjacency_matrix, nodes, obstacles)

        # Add observations to nodes
        T_obs = {}
        for node in nodes:
            if node == initial_state:
                T_obs[node] = 'o1'  # Observation of initial state
            elif node in rois:
                T_obs[node] = 'o2'  # Observation of regions of interest
            elif node in obstacles:
                T_obs[node] = 'o3'  # Observation of obstacles
            elif node == final_state:
                T_obs[node] = 'o4'  # Observation of final state
            else:
                T_obs[node] = 'e'  # Empty/free space

        return g, pruned_adjacency_matrix, T_obs

    def plot_graph(self, g, obstacles, rois, initial_state, final_state, path=None):
        # Plotting the graph
        pos = dict((n, (n[1], -n[0])) for n in g.nodes())
        node_colors = []
        for node in g.nodes():
            if node == initial_state:
                node_colors.append('orange')
            elif node in rois:
                node_colors.append('green')
            elif node in obstacles:
                node_colors.append('red')
            elif node == final_state:
                node_colors.append('gray')
            else:
                node_colors.append('white')

        nx.draw(g, pos, with_labels=True, node_size=500, node_color=node_colors)

        # Highlight the path
        if path:
            edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(g, pos, edgelist=edges, edge_color='blue', width=2)

        plt.show()

    def shortest_path(self, g, start, end):
        # Find the shortest path using Dijkstra's algorithm
        return nx.shortest_path(g, source=start, target=end, weight='weight')

    def compute_path_with_roi(self, g, initial_state, rois, final_state):
        # Find the shortest path to a chosen ROI, then to the final state
        chosen_roi = rois[0]  # For simplicity, select the first ROI
        path_to_roi = self.shortest_path(g, initial_state, chosen_roi)
        path_to_final = self.shortest_path(g, chosen_roi, final_state)
        return path_to_roi + path_to_final[1:]  # Concatenate paths


def main():
    rows = 5
    cols = 4
    

    # Obstacles (red cells)
    obstacles = [(1, 1), (2, 1)]

    # Regions of Interest (green cells)
    rois = [(0, 2), (4, 1)]

    # Initial and Final States
    initial_state = (4, 3)  # Orange cell
    final_state = (0, 3)  # Gray cell

    hw = Homework1()
    G, adj_matrix, T_obs = hw.create_graph(rows, cols, obstacles, rois, initial_state, final_state)
    
    print("Adjacency matrix:\n", adj_matrix)
    print("Observations of nodes:", T_obs)
    print(G)

    # Task 1: Shortest path from initial state to final state
    path1 = hw.shortest_path(G, initial_state, final_state)
    print("Task 1 - Shortest path from initial to final state:", path1)
    print("Input/Output words:", [T_obs[node] for node in path1])
    hw.plot_graph(G, obstacles, rois, initial_state, final_state, path1)

    # Task 2: Shortest path via a desired region
    path2 = hw.compute_path_with_roi(G, initial_state, rois, final_state)
    print("Task 2 - Shortest path via desired region:", path2)
    print("Input/Output words:", [T_obs[node] for node in path2])
    hw.plot_graph(G, obstacles, rois, initial_state, final_state, path2)


if __name__ == "__main__":
    main()
