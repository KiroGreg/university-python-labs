"""
Laboratory Work 4: Graph Structure Analysis
Analyzes graph connectivity, degrees, eccentricity, diameter, radius, and spanning trees using NetworkX and Matplotlib.
"""

import matplotlib.pyplot as plt
import networkx as nx

def main():
    graph1 = nx.Graph()
    all_nodes = list(range(15))
    graph1.add_nodes_from(all_nodes)
    
    edges = [
        (0, 1), (1, 2), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (7, 10),
        (8, 9), (9, 10), (11, 9), (10, 11), (12, 13), (13, 14), (14, 12), (2, 0),
        (7, 8), (11, 7), (11, 8), (7, 9), (8, 10), (6, 5)
    ]
    graph1.add_edges_from(edges)
    
    positions = nx.spring_layout(graph1, k=1)
    nx.write_edgelist(graph1, "graph.txt")
    
    # Figure 1: General graph and metrics
    plt.figure(figsize=(8, 6))
    nx.draw(graph1, pos=positions, with_labels=True, node_color="white", edgecolors="black")
    plt.text(-1.2, 1, f"""Nodes: {graph1.number_of_nodes()}
Edges: {graph1.number_of_edges()}
Connected Components: {nx.number_connected_components(graph1)}""")
    plt.savefig("graph1.png")
    plt.close()

    # Figure 2: Shell layout from edgelist
    graph2 = nx.read_edgelist("graph.txt", nodetype=int)
    pos2 = nx.shell_layout(graph2)
    plt.figure(figsize=(8, 6))
    nx.draw(graph2, pos=pos2, with_labels=True, node_color="white", edgecolors="black")
    plt.savefig("graph2.png")
    plt.close()

    # Figure 3: Planar modification discussion
    graph3 = graph1
    custom_positions = {
        0: (0, 1), 1: (0, 0), 2: (1, 0), 3: (2, 0), 4: (2.5, 1),
        5: (2.5, 0.3), 6: (3, 0), 7: (5.1, 0.6), 8: (5, 1), 9: (4, 0),
        10: (4.8, 0.3), 11: (6, 0), 12: (7, 1), 13: (7, 0), 14: (8, 0)
    }
    plt.figure(figsize=(10, 6))
    nx.draw(graph3, pos=custom_positions, with_labels=True, node_color="white", edgecolors="black")
    plt.title("Removing one edge (e.g., (8, 10)) makes the graph planar.")
    plt.savefig("graph3.png")
    plt.close()

    # Component Analysis
    graph4 = graph1
    components = nx.connected_components(graph4)

    for component_idx, node_set in enumerate(components):
        graph_component = graph4.subgraph(node_set)
        nodes_degrees = dict(graph_component.degree())
        nodes_eccentricity = nx.eccentricity(graph_component)
        print(f"\nComponent {component_idx + 1}")
        print(f"  Nodes: {nx.number_of_nodes(graph_component)}")
        print(f"  Edges: {nx.number_of_edges(graph_component)}")
        print("  Degrees:")
        for node, degree in nodes_degrees.items():
            print(f"    Degree of node '{node}': {degree}")
        print("  Eccentricities:")
        for node, eccentricity in nodes_eccentricity.items():
            print(f"    Eccentricity of node '{node}': {eccentricity}")
        print(f"  Radius: {min(nodes_eccentricity.values())}")
        print(f"  Diameter: {max(nodes_eccentricity.values())}")

    # Figure 5: Diameters highlighted
    graph5 = graph1
    nontrivial_components = nx.connected_components(graph5)
    all_path = []
    for nodes in nontrivial_components:
        sub_graph = graph5.subgraph(nodes)
        periphery = nx.periphery(sub_graph)
        if periphery:
            path = nx.shortest_path(sub_graph, periphery[0], periphery[1])
            all_path += path
            
    nodes_color = ["blue" if node in all_path else "white" for node in nx.nodes(graph5)]
    edges = graph5.edges()
    edges_color = ["blue" if edge[0] in all_path and edge[1] in all_path else "black" for edge in edges]
    
    plt.figure(figsize=(8, 6))
    nx.draw(graph5, pos=custom_positions, with_labels=True, node_color=nodes_color, edge_color=edges_color, edgecolors="black")
    plt.title("Diameters (blue nodes and edges highlight diameter paths)")
    plt.savefig("graph_diameters.png")
    plt.close()

    # Figure 6: Depth-first search forest / spanning tree
    graph6 = graph1
    forest = nx.Graph(nx.dfs_tree(graph6))
    edges_color_forest = ["red" if edge in forest.edges or (edge[1], edge[0]) in forest.edges else "black" for edge in graph6.edges]
    nodes_color_white = ["white" for _ in graph6.nodes]
    
    plt.figure(figsize=(8, 6))
    nx.draw(graph6, with_labels=True, pos=custom_positions, node_color=nodes_color_white, edge_color=edges_color_forest, edgecolors="black")
    plt.title("Depth-First Search Spanning Forest (red edges)")
    plt.savefig("graph_dfs_forest.png")
    plt.close()
    print("\nGraph analysis completed successfully. All plots saved.")


if __name__ == "__main__":
    main()
