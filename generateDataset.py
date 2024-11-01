import numpy as np


def read_graph(file_path):
    edges = []  # List to store the tuples (FromNodeId, ToNodeId)

    with open(file_path, 'r') as file:
        for line in file:
            # Skip lines that start with '#'
            if line.startswith('#'):
                continue

            # Split the line by tab or space and convert the two values to integers
            parts = line.split()
            if len(parts) == 2:  # Ensure there are two elements (FromNodeId, ToNodeId)
                from_node = int(parts[0])
                to_node = int(parts[1])
                edges.append((from_node, to_node))  # Add the tuple to the list

    return edges

file_path = 'web-Google.txt'
MaxId = 650000
outFile = "mediumDataset.txt"
nodes = set()
newEdges = list()
edges = read_graph(file_path)

with open(outFile, "w") as file:
    for item in edges:
        if item[0]<MaxId and item[1]<MaxId:
            nodes.add(item[0])
            nodes.add(item[1])
            newEdges.append([item[0],item[1]])
            file.write(f"{item[0]}  {item[1]}\n")
    file.write(f"#Nodes: {len(nodes)} Edges: {len(newEdges)}")
