import networkx as nx
G = nx.Graph()

usa = open('contiguous-usa.dat')
for line in usa:
    s1, s2 = line.strip().split()
    G.add_edge(s1, s2)

for state in G.nodes():
    if state != 'CA':
        G.node[state]['demand'] = 1
G.node['CA']['demand'] = -48

G = nx.DiGraph(G)
uniform_capacity = 16
for (s1, s2) in G.edges():
    G.edges[s1, s2]['capacity'] = uniform_capacity

def flow_with_demands(graph):
    """Computes a flow with demands over the given graph.
    
    Args:
        graph: A directed graph with nodes annotated with 'demand' properties and edges annotated with 'capacity' 
            properties.
        
    Returns:
        A dict of dicts containing the flow on each edge. For instance, flow[s1][s2] should provide the flow along
        edge (s1, s2).
        
    Raises:
        NetworkXUnfeasible: An error is thrown if there is no flow satisfying the demands.
    """
    # TODO: Implement the function.
    
    # add super source node and super sink node 
    graphNew=graph.copy()

    graphNew.add_node('s')
    graphNew.add_node('t')
    graphNew.node['s']['demand'] = 0
    graphNew.node['t']['demand'] = 0   
    
    f=0
    
    # add adajcent edges and assign capacities
    for state in graphNew.nodes():
        d=graphNew.node[state]['demand']
        if d < 0:
            graphNew.add_edge('s',state)
            graphNew.edges['s',state]['capacity']=-d
            # compute the sum of demands 
            f=f-d
        if d > 0:
            graphNew.add_edge(state,'t')
            graphNew.edges[state,'t']['capacity']=d
    
    def InitializeFlow_dict():
        flow_dict={}
        for state in graphNew.nodes():
            d={state:{}}
            flow_dict.update(d)
    
        for u,v in graphNew.edges():
            d={v:0}
            flow_dict[u].update(d)
        return(flow_dict)
    
    graphR= nx.DiGraph()

    # compute residual graph
    def ComputeGraphR(graphNew,flow_dict):
        for state in graphNew.nodes():
            graphR.add_node(state)
        for u,v in graphNew.edges():
            if flow_dict[u][v]<graphNew.edges[u,v]['capacity']:
                graphR.add_edge(u,v)
                graphR.edges[u,v]['capacity']=graphNew.edges[u,v]['capacity']-flow_dict[u][v]
            if flow_dict[u][v]>0:
                graphR.add_edge(v,u)
                graphR.edges[v,u]['capacity']=flow_dict[u][v]
        return(graphR)
    
    # DFS to find s-t path in residual graph
    # def DFS(graphR):
    #     if start == goal:
    #     return [start]
    #     visited = {start}
    #     queue = deque([(start, [])])

    #     while queue:
    #         current, path = queue.popleft()
    #         visited.add(current)
    #         for neighbor in graph[current]:
    #             if neighbor == goal:
    #                 return path + [current, neighbor]
    #             if neighbor in visited:
    #                 continue
    #             queue.append((neighbor, path + [current]))
    #             visited.add(neighbor)   
    #     return None  # no path found. not strictly needed
    #     s=[]
    #     s.append('s')
    #     visited=[]
    #     path=[]
    #     while len(s)>0:
    #         u=s.pop()
    #         visited.append(u)
    #         for v in graphR.neighbors(u):
    #             if v=='t':
    #                 return(path.append((u,v)))
    #             if v in visited:
    #                 continue
    #             s.append(v)
    #             path.append((u,v))
    #                                                                                                         flow_dict=InitializeFlow_dict()
    
    
    # graphR=ComputeGraphR(graphNew,flow_dict)
    # path=DFS(graphR)
    
    # # augment path
    # def AugmentPath(graphNew,graphR,flow_dict,path):
    #     bottleneck=min(graphR.edges[u,v]['capacity'] for (u,v) in path)
    #     for u,v in path:
    #         if u,v in graphNew.edges():
    #             flow_dict[u][v]=flow_dict[u][v]+bottleneck
    #         if v,u in graphNew.edges():
    #             graphNew.add_edge(u,v)
    #             d1={u:{}}
    #             flow_dict.update(d1)
    #             d2={v:0}
    #             flow_dict[u].update(d2)
    #             flow_dict[u][v]=



    a=0
    # use bfs to find s-t path
    # path=[]
    # visited=[]
    # path.append['s'] 
    # while path:
    #     u=path.pop()
    #     if u not in visited:
    #         visited.append(u)
    #         for u,v in graphNew:
    #             if neighbor not in visited:
    #                 s.append(neigA/.A/hbor)

    # def bfs(graph, start, end):
    # # maintain a queue of paths
    # queue = []
    # visited=[]

    # flow_value, flow_dict = nx.maximum_flow(graphNew, 's', 't',capacity='capacity')
    # del flow_dict['s']
    # del flow_dict['t']
    
    # for s1 in list(flow_dict):
    #     for s2 in list(flow_dict[s1]):
    #         if s2 =='t':
    #             del flow_dict[s1]['t']
    
    # return(flow_dict)
    # if flow_value == f:
    #     return(flow_dict)
    # else:
    #     raise ValueError('NetworkXUnfeasible')
    return()

def divergence(flow):
    """Computes the total flow into each node according to the given flow dict.
    
    Args:
        flow: the flow dict recording flow between nodes.
        
    Returns:
        A dict of the net flow into each node.
    """
    # TODO: Implement the function.
    
    div=dict()
    for state in flow.keys():
        div[state]=0

    for s1 in div.keys():
        for s2 in flow[s1].keys():
            div[s1]=div[s1]-flow[s1][s2]
            div[s2]=div[s2]+flow[s1][s2]

    return(div)

flow=flow_with_demands(G)

div=divergence(flow)
print(div)