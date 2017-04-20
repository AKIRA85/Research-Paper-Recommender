import json
import networkx as nx

st_time=int(input('Enter start Time:'))
en_time=int(input('Enter End Time:'))

author_index_file_path = 'author_index_dict.json'
paper_file_path = 'Database.txt'
author_citation_graph_file_path = 'author-citation-graph.edgelist'

author_index_dict = json.load(open(author_index_file_path,'r'))

author_citation_graph = nx.DiGraph()

with open(paper_file_path, 'r') as paper_file:
    active_index=-1
    count_line=0
    authors = ""
    for line in paper_file:
        if count_line%100000==0:
            print count_line
        count_line+=1
        if '#index' in line:
            active_index=line[7:-1]
        elif '#@' in line:
            authors=line[3:-1]
        elif '#t' in line:
            try:
                time=int(line[3:-1])
            except:
                time=2055  #@akshay what to do when time is not known
        elif '#%' in line and time>=st_time and time<=en_time:
            ref=line[3:-1]
            for author in authors.split(";"):
                if author in author_index_dict:
                    author_citation_graph.add_edge("@"+str(author_index_dict[author]), "#"+ref)

nx.write_edgelist(author_citation_graph, author_citation_graph_file_path)