# CSCI596 Final Project: Parallel Computing based PageRank Optimization
This is a readme file for the Parallel Computing based PageRank Optimization project. 
This project implements an optimized version of the PageRank algorithm, leveraging parallel processing techniques to enhance efficiency in large-scale graph computations.

### Introduction to PageRank
Originally developed by Google, the PageRank algorithm is a graph-based ranking method that assigns relative importance to nodes (e.g., web pages) based on their link structure. Each node's rank is determined by the ranks of nodes linking to it, with the goal of identifying influential nodes in a network. By iteratively distributing rank scores across links, PageRank helps surface high-authority pages in web search, making it foundational in information retrieval and network analysis.

### About This Project
This project uses PySpark to parallelize the iterative PageRank computation, optimizing for both runtime and scalability. Key features include:
* Parallelized Iterative Computation: Efficiently handles multiple iterations across distributed nodes.
* Optimized Data Collection: Minimizes data shuffling to reduce overhead.
* Flexible Configuration: Allows easy tuning for various graph sizes and cluster configurations.
This implementation is ideal for high-volume datasets in applications such as web search, social network analysis, and recommendation systems. 

## 0. Prerequisites
Only needed is C compiler.
## 1. How to compile and run
If the C compiler on your computer is cc (also common is gcc for Gnu C
compiler), type:
cc -O -o md md.c -lm
This will create an executable named md. To run the executable, type:
./md < md.in
## 2. Files
The following files are included in this folder, in addition to this readme
file, readme.md.
<ul>
<li>md.c: Main C program</li>
<li>md.h: Header file for md.c</li>
<li>md.in: Input parameter file (to be redirected to the standard input)</li>
</ul>
![Screen shot of MD simulation](ScreenShot.png)

## 3. Experiment
count time: decrease the abnormal time caused by system
1. different size of the datasets
    * 100000X
    * 200000X
    * ...
    * 800000X
    <br> efficiency
2. impact of different threads

Placeholder for project initialization
