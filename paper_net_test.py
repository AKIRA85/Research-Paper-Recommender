import networkx as nx
# import pandas as pd

st_time=int(input('Enter start Time:'))
en_time=int(input('Enter End Time:'))

paper_file_path = 'Database.txt'
# paper_file_path = 'AMiner-Paper.txt'
paper_author_file_path = 'paper-author.csv'
paper_citation_graph_file_path = 'paper-citation-graph.edgelist'

paper_citation_network=nx.DiGraph()   
paper_author_dict = dict()
columns = ['paper_index', 'author_names']
# paper_author_df = pd.DataFrame(columns=columns)

with open(paper_file_path, 'r') as paper_file:
    active_index=-1
    count_line=0
    for line in paper_file:
        if count_line%100000==0:
            print count_line
        count_line+=1
        if '#index' in line:
            active_index=line[7:-1]
        elif '#@' in line:
            authors=line[3:-1]
            paper_author_dict[active_index]=set(authors.split(";"))

with open(paper_file_path, 'r') as paper_file:
    active_index=-1
    count_line=0
    for line in paper_file:
        if count_line%100000==0:
            print count_line
        count_line+=1
        if '#index' in line:
            active_index=line[7:-1]
        elif '#t' in line:
            try:
                time=int(line[3:-1])
            except:
                time=2055  #@akshay what to do when time is not known
        elif '#%' in line and time>=st_time and time<=en_time:
            ref=line[3:-1]
            if active_index in paper_author_dict and ref in paper_author_dict:
                if len(paper_author_dict[active_index].intersection(paper_author_dict[ref]))==0:
                    paper_citation_network.add_edge(active_index, ref)

nx.write_edgelist(paper_citation_network, paper_citation_graph_file_path)
# paper_author_df.to_csv(paper_author_file_path, sep=', ')

with open(paper_author_file_path, 'w') as output_file:
    count_line = 0
    for key, value in paper_author_dict.iteritems():
        if count_line%100000==0:
            print count_line
        count_line+=1
        s = key+">>"+';'.join(value)+"\n"
        output_file.write(s)
