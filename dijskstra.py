from collections import defaultdict 
  
class Graph: 
  
    def minDistance(self,dist,queue): 
        minimum = float("Inf") 
        min_index = -1
          
        for i in range(len(dist)): 
            if dist[i] < minimum and i in queue: 
                minimum = dist[i] 
                min_index = i 
        return min_index 
  
    def printPath(self, parent, j): 
          
        if parent[j] == -1 :  
            print j, 
            return
        self.printPath(parent , parent[j]) 
        print j, 
          
  
    def printSolution(self, dist, parent): 
        src = 0
        print("s --> d\t\t rtt \tpath") 
        print("\n%d-->%d\t\t%d \t" % (src, 4, dist[4])), 
        self.printPath(parent,4) 
  
    def dijkstra(self, graph, src): 
  
        row = len(graph) 
        col = len(graph[0]) 
  
        dist = [float("Inf")] * row 
  
        parent = [-1] * row 
  
        dist[src] = 0
      
        queue = [] 
        for i in range(row): 
            queue.append(i) 
              
        while queue: 
  
            u = self.minDistance(dist,queue)  
  
            queue.remove(u) 
            for i in range(col): 
                if graph[u][i] and i in queue: 
                    if dist[u] + graph[u][i] < dist[i]: 
                        dist[i] = dist[u] + graph[u][i] 
                        parent[i] = u 
  
  
        self.printSolution(dist,parent) 
  
g= Graph() 

graph = [[0,1,3,1,0],
        [1,0,5,0,1],
        [3,5,0,4,1],
        [1,0,4,0,2],
        [0,1,1,2,0]]
  
g.dijkstra(graph,0) 
