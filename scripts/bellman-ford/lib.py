#!/usr/bin/python

def print_by_node(pred, origin, dest, path):
  if dest == origin:
    return path
  else:
    next_node = pred[dest]
    return print_by_node(pred, origin, next_node, "%s ,%d" % (path, next_node + 1))

def read_graph():
  entry = open('grafo.txt', 'r')

  graph = []
  for index, line in enumerate(entry.readlines()):
    if index == 0:
      n = int(line)
      # weight_matrix = np.zeros(shape=(n, n), dtype='i')
    else:
      a, b, w = line.rstrip().split(' ')
      if 'a' in a.lower(): a = a[1:]
      if 'b' in b.lower(): b = b[1:]
      x_idx = int(a) - 1
      y_idx = int(b) - 1
      graph.append([x_idx, y_idx, int(w)])
      graph.append([y_idx, x_idx, int(w)])

  return n, graph

def bellman_ford(graph, n, origin):
  # Step 1: Initialize distances from src to all other vertices 
  # as INFINITE 
  dist = [float('Inf')] * n
  pred = [None] * n
  dist[origin] = 0 

  # Step 2: Relax all edges |V| - 1 times. A simple shortest  
  # path from src to any other vertex can have at-most |V| - 1  
  # edges 
  for i in range(n): 
    # Update dist value and parent index of the adjacent vertices of 
    # the picked vertex. Consider only those vertices which are still in 
    # queue 
    for a, b, w in graph: 
      if dist[a] != float('Inf') and dist[a] + w < dist[b]: 
        dist[b] = dist[a] + w 
        pred[b] = a

  # Step 3: check for negative-weight cycles. The above step  
  # guarantees shortest distances if graph doesn't contain  
  # negative weight cycle. If we get a shorter path, then there 
  # is a cycle. 

  for a, b, w in graph:
    if dist[a] != float('Inf') and dist[a] + w < dist[b]: 
      print('Graph contains negative weight cycle')
      return None, None

  return dist, pred

def write_vertex(n, pred, origin):
  if pred is not None and origin is not None:
    print("V%d:" % (origin + 1))
    for node in range(n):
      print("%d: %s" % (node + 1, print_by_node(pred, origin, node, "%d" % (node + 1))[::-1]))
    print("\n")
