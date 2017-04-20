import networkx as nx

random_walk_graph_file_path = 'random_walk_graph.edgelist'
author_citation_graph_file_path = 'author-citation-graph.edgelist'
author_paper_file_path = 'author-paper.csv'

author_random_walk_trust_graph = paper_citation_graph = nx.read_edgelist(random_walk_graph_file_path)
author_random_walk_trust_matrix = nx.adjacency_matrix(author_random_walk_trust_graph, weight='weight')
authors = author_random_walk_trust_graph.nodes()

author_citation_graph = nx.read_edgelist(author_citation_graph_file_path)
authors = author_random_walk_trust_graph.nodes()
author_paper_graph = nx.DiGraph()

with open(author_paper_file_path, 'r') as author_paper_file:
    for line in author_paper_file:
        l = line.split(", ")
        author_paper_graph.add_edge("@"+l[0], "#"+l[1])

author_ids = set()
print author_citation_graph.nodes()
for node in author_citation_graph.nodes():
    print node
    if "@" in node:
        author_ids.add(node[1:])
print author_ids

print "common", len(author_ids.intersection(set(authors)))

for i in range(50):
    print i
    if author_citation_graph.has_node("@"+authors[i]):
        citations = author_citation_graph.neighbors("@"+authors[i])
        print "citation count", len(citations)
        if len(citations)>5:
            trust_array = author_random_walk_trust_matrix.getrow(i).toarray()[0]
            trusted_authors = np.argpartition(trust_array, 10)[0:10]
            paper_count=0
            for x in trusted_authors:
                paper_count+=author_paper_graph.neighbors("@"+authors[x])
            print paper_count
    # else:
        # print "no citations"

