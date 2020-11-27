import collections

#This code modifies the MaximumFlow project to find the minimum cuts of a graph as well.

#The main logic involves creating a copy of the original graph to compare the residual capacities of the worked graph
#Any edges that originally had capacity but now have 0 residual capacity are the minimum cuts

class Graph(object):
    """Instantiates a graph object based on an adjacency matrix supplied
    in the form of a list of lists."""

    def __init__(self, adjacency_matrix, adjacency_matrix_copy):
        self.graph = adjacency_matrix  # original copy
        self.residual = adjacency_matrix_copy
        self.row = len(adjacency_matrix)

    def bfs(self, s, t, path):
        """
        Breadth-first search of the graph.
        Returns true if there is a path from source 's' to sink 't' in
        residual graph. The path is stored in path[]"""

        # Mark all the vertices as not visited
        visited = [False] * self.row

        # Create a queue for BFS
        queue = collections.deque()

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BFS loop
        while queue:
            u = queue.popleft()

            # Get all adjacent vertices of the dequeued vertex u
            # If an adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.residual[u]):
                if (visited[ind] == False) and (val > 0):
                    queue.append(ind)
                    visited[ind] = True
                    path[ind] = u

        # If we reached sink in BFS starting from source, then return
        # true, else false
        return visited[t]

    # Returns the maximum flow from s to t in the given graph
    def Ford_Fulkerson(self, source, target):

        # This array is filled by BFS and to store path
        s_t_path = [-1] * self.row

        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from source to sink
        while self.bfs(source, target, s_t_path):

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = target
            while s != source:
                # the path flow is the capacity of the edge with the min capacity.
                path_flow = min(path_flow, self.residual[s_t_path[s]][s])
                s = s_t_path[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path. In this updated version, let's make this a new graph since we need the original one.
            v = target
            while v != source:
                u = s_t_path[v]
                self.residual[u][v] -= path_flow
                self.residual[v][u] += path_flow
                v = s_t_path[v]
            # the edges that are now zero must have been the 'limiting reagents' and therefore the minimum cuts
            # to find them, we can compare the residual capacities to the original capacities:
        min_cut_pair = []
        print('Original Graph: ')
        print(self.graph)
        print('Residual Capacities: ')
        print(self.residual)
        for row in range(len(self.graph)):
            for col in range(len(self.graph[0])):
                if self.residual[row][col] == 0 and self.graph[row][col] != 0:
                    min_cut_pair.append([row, col])
                    #print('row ' + str(row))
                    #print('col ' + str(col))
        return max_flow, min_cut_pair



# Sample adjacency matrix given as a list of lists; one list per node;
# the list contains the edge capacities from the node to the other nodes.
# For example, the second element of the 3rd list is the capacity of
# the edge from node(2) to node(1).

# Node:   0   1   2   3   4   5   # node
graph = [[0, 16, 13,  0,  0,  0], # 0
         [0,  0, 10, 12,  0,  0], # 1
         [0,  4,  0,  0, 14,  0], # 2
         [0,  0,  9,  0,  0, 20], # 3
         [0,  0,  0,  7,  0,  4], # 4
         [0,  0,  0,  0,  0,  0]] # 5

# Node:   0   1   2   3   4   5   # node
graphCopy = [[0, 16, 13,  0,  0,  0], # 0
         [0,  0, 10, 12,  0,  0], # 1
         [0,  4,  0,  0, 14,  0], # 2
         [0,  0,  9,  0,  0, 20], # 3
         [0,  0,  0,  7,  0,  4], # 4
         [0,  0,  0,  0,  0,  0]] # 5

# Instantiate a Graph object using the adjacency list above
g = Graph(graph, graphCopy)

# Declare source and target vertices
source = 0; # source
target = 5; # target

# compute the maximum flow between source and target
mf, mins = g.Ford_Fulkerson(source, target)
print('Maximum Flow: ')
print(mf)
print('Minimal Cuts: ')
print(mins)
