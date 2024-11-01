import sys
from operator import add
from typing import Iterable, Tuple
from pyspark.resultiterable import ResultIterable
from pyspark.sql import SparkSession
import os
import time

os.environ['PYSPARK_PYTHON'] = sys.executable

# n_threads = 4  # Number of local threads
n_iterations = 10  # Number of iterations
q = 0.15 #the default value of q is 0.15

def computeContribs(neighbors: ResultIterable[int], rank: float) -> Iterable[Tuple[int, float]]:
    # Calculates the contribution(rank/num_neighbors) of each vertex, and send it to its neighbours.
    num_neighbors = len(neighbors)
    for vertex in neighbors:
        yield (vertex, rank / num_neighbors)

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

def compute_rank(file_name, n_threads):
    print(f"compute rank in dataset: {file_name} with {n_threads} threads")
    # Initialize the spark context.
    file_path = file_name + '.txt'
    edges_list = read_graph(file_path)
    spark = SparkSession\
        .builder\
        .appName("PageRank")\
        .master("local[%d]" % n_threads)\
        .getOrCreate()
    print(f"spark init")
    startTime = time.time()
    # link: (source_id, dest_id)
    links = spark.sparkContext.parallelize(
        edges_list,
    )

    # drop duplicate links and convert links to an adjacency list.
    adj_list = links.distinct().groupByKey().cache()

    # count the number of vertexes
    n_vertexes = adj_list.count()

    # init the rank of each vertex, the default is 1.0/n_vertexes
    ranks = adj_list.map(lambda vertex_neighbors: (vertex_neighbors[0], 1.0/n_vertexes))

    print(f"start iterate")
    # Calculates and updates vertex ranks continuously using PageRank algorithm.
    for t in range(n_iterations):
        # Calculates the contribution(rank/num_neighbors) of each vertex, and send it to its neighbours.
        contribs = adj_list.join(ranks).flatMap(lambda vertex_neighbors_rank: computeContribs(
            vertex_neighbors_rank[1][0], vertex_neighbors_rank[1][1]  # type: ignore[arg-type]
        ))

        # Re-calculates rank of each vertex based on the contributions it received
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: q/n_vertexes + (1 - q)*rank)

    output_file_name = 'TestResult/test_result_{}_{}.txt'.format(file_name, n_threads)
    vertex_rank = []
    endTime = time.time()
    # Collects all ranks of vertexs and dump them to console.
    for (vertex, rank) in ranks.collect():
        vertex_rank.append((vertex, rank))
        # print("%s has rank: %s." % (vertex, rank))
    process_time = time.time()
    spark.stop()
    print(f"output result")
    vertex_rank.sort(key=lambda pair: pair[1], reverse=True)
    with open(output_file_name, "w") as file:
        file.write(f"vertex  rank\n")
        for (vertex, rank) in vertex_rank:
            file.write(f"{vertex}  {rank}\n")
        file.write(f"caltime:  {endTime - startTime}\n")
        file.write(f"process:  {process_time - startTime}\n")




test_config = [('smallDataset', 1), ('smallDataset', 2), ('smallDataset', 4), ('smallDataset', 8), ('smallDataset', 16),
               ('mediumDataset', 1), ('mediumDataset', 2), ('mediumDataset', 4), ('mediumDataset', 8), ('mediumDataset', 16),
               ('web-Google', 1), ('web-Google', 2), ('web-Google', 4), ('web-Google', 8), ('web-Google', 16),]
for (file_name, n_threads) in test_config:
    compute_rank(file_name, n_threads)
    time.sleep(3)
    

