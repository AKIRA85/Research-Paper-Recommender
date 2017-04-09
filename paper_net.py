import networkx as nx

st_time=int(input('Enter start Time:'))
en_time=int(input('Enter End Time:'))

# paper_file_path = 'Database.txt'
paper_file_path = 'AMiner-Paper.txt'

paper_citation_network=nx.DiGraph()   
paper_author_dict = dict()

count_line=0
with open(paper_file_path) as paper_file:
    if count_line%100==0:
        print count_line
    count_line+=1
    active_index=-1
    for line in paper_file:
        if '#index' in line:
            active_index=line[7:-1]
        if '#@' in line:
            authors=line[3:-1]
            paper_author_dict[active_index]=set(authors.split(";"))
        if '#t' in line:
            try:
                time=int(line[3:-1])
            except:
                time=2055  #@akshay what to do when time is not known
        if '#%' in line and time>=st_time and time<=en_time:
            ref=line[3:-1]
            add_edge_flag = False
            if active_index in paper_author_dict and ref in paper_author_dict:
                add_edge_flag = len(paper_author_dict[active_index].intersection(paper_author_dict[ref]))==0
            else:
                add_edge_flag = True
            if add_edge_flag:
                paper_citation_network.add_edge(active_index, ref)

nx.write_edgelist(paper_citation_network, "test.edgelist")