import networkx as nx
import numpy as np
from sklearn.preprocessing import normalize
from scipy.sparse import linalg
from scipy import sparse
from random import random

gamma = 0.8
walker_count = 100

author_trust_graph_file_path = 'author_trust_graph.edgelist'
random_walk_graph_file_path = 'random_walk_graph.edgelist'

author_trust_graph = nx.read_edgelist(author_trust_graph_file_path)
adjacency_matrix = nx.adjacency_matrix(author_trust_graph, weight='total')
normalized_adjacency_matrix = normalize(adjacency_matrix, norm='l1', axis=1)
# I = sparse.identity(adjacency_matrix.shape[0])
# inverse = linalg.inv(sparse.csc_matrix(I - 0.7*normalized_adjacency_matrix))
# H = inverse*normalized_adjacency_matrix
# print H.getrow(0)
mapping = {i:j for i,j in enumerate(author_trust_graph.nodes())}
node_count = adjacency_matrix.shape[0]
hit_matrix = np.zeros((node_count, node_count))

for i in range(walker_count):
    print i,
    walker_position = np.array(range(node_count))
    prob_matrix = normalized_adjacency_matrix
    index = np.where(walker_position>-1)[0]
    while len(index)>0:
        # print walker_position
        x = np.random.random_sample((node_count,))
        for i in index:
            prob = prob_matrix.getrow(walker_position[i]).toarray()[0]
            bins = np.insert(np.cumsum(prob[prob.nonzero()]), 0, 0)
            step, bins = np.histogram([x[i]], bins=bins)
            # print x
            # print prob
            # print bins
            # print step
            # print step.nonzero()
            if len(step.nonzero()[0])==0:
                walker_position[i]=-1
            else:
                jump_to = prob.nonzero()[0][step.nonzero()[0][0]]
                hit_matrix[i][jump_to]+=1
                walker_position[i]=jump_to
        index = np.where(walker_position>-1)[0]
        prob_matrix = gamma*prob_matrix

print "done"

author_random_walk_trust_graph=nx.from_numpy_matrix(normalize(hit_matrix, norm='l1', axis=1))
nx.relabel_nodes(author_random_walk_trust_graph,mapping,copy=False)
nx.write_edgelist(author_random_walk_trust_graph, random_walk_graph_file_path)