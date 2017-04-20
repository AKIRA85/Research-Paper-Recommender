import networkx as nx
import pandas as pd
import json

author_file_path = 'AMiner-Author.txt'
author_index_file_path = 'author_index_dict.json'
paper_author_file_path = 'paper-author.csv'
author_paper_file_path = 'author-paper.csv'
author_trust_graph_file_path = 'author_trust_graph.edgelist'
paper_citation_graph_file_path = 'paper-citation-graph.edgelist'

print "reading author data file"
author_index_dict=dict()
with open(author_file_path, 'r') as author_file:
    count_line = 0
    for line in author_file:
        if count_line%1000000==0:
            print count_line
        count_line+=1
        if '#index' in line:
            index=line[7:-1]
        elif '#n' in line:
            author=line[3:-1]
            author_index_dict.update({author:int(index)})

json.dump(author_index_dict, open(author_index_file_path,'w'))

print "reading paper author dataframe"
paper_author_df = pd.read_csv(paper_author_file_path, 
                header=0, 
                names=['paper_index', 'author_names'], 
                sep='>>', 
                engine='python').fillna(0)

print "reading paper citation graph"
paper_citation_graph = nx.read_edgelist(paper_citation_graph_file_path)
author_trust_graph = nx.DiGraph()

print "creating citation edges"
egde_count=0
print len(paper_citation_graph.edges())
for edge in paper_citation_graph.edges_iter():
    if egde_count%100==0:
        print egde_count
    egde_count+=1
    citing_author_names = paper_author_df[paper_author_df['paper_index']==int(edge[0])]['author_names'].iloc[0]
    cited_author_names = paper_author_df[paper_author_df['paper_index']==int(edge[1])]['author_names'].iloc[0]
    # print "this", cited_author_names
    if citing_author_names!=0 and cited_author_names!=0:
        citing_author_list = citing_author_names.split(";")
        cited_author_list = cited_author_names.split(";")
        for citing_author in citing_author_list:
            if citing_author in author_index_dict:
                for cited_author in cited_author_list:
                    if cited_author in author_index_dict:
                        citing_author_index = author_index_dict[citing_author]
                        cited_author_index = author_index_dict[cited_author]
                        if author_trust_graph.has_edge(citing_author_index, cited_author_index):
                            author_trust_graph[citing_author_index][cited_author_index]['citation']+=1
                        else:
                            author_trust_graph.add_edge(citing_author_index, cited_author_index, citation=1,collab=0,total=0)

paper_indexes = map(int, paper_citation_graph.nodes())
print "accepted papers count :", len(paper_indexes)
print paper_author_df[paper_author_df['paper_index'].isin(paper_indexes)]

print "creating collaboration edges and author paper file"

row_count=0
with open(author_paper_file_path, "w") as author_paper_file:
    for row in paper_author_df[paper_author_df['paper_index'].isin(paper_indexes)][['paper_index', 'author_names']].itertuples():
        # print row[2]
        if row_count%100==0:
            print row_count
        row_count+=1
        if row[2]==0:
            continue
        author_list = row[2].split(';')
        for i in range(len(author_list)):
            if author_list[i] in author_index_dict:
                author_paper_file.write(str(author_index_dict[author_list[i]])+", "+str(row[1])+"\n")
            for j in range(len(author_list)):
                if i!=j and author_list[i] in author_index_dict and author_list[j] in author_index_dict:
                    index_i = author_index_dict[author_list[i]]
                    index_j = author_index_dict[author_list[j]]
                    if author_trust_graph.has_edge(index_i, index_j):
                        author_trust_graph[index_i][index_j]['collab']+=1
                    else:
                        author_trust_graph.add_edge(index_i, index_j, citation=0,collab=1,total=0)

for edge in author_trust_graph.edges_iter(data=True):
    edge[2]['total'] = 0.6*edge[2]['citation']+0.4*edge[2]['collab']

nx.write_edgelist(author_trust_graph, author_trust_graph_file_path)

# fp=open('Database.txt','r')
# of=open('Paper_citation_network_Database.txt','w')
# of1=open('collaboration_author_Database.txt','w')
# c=fp.readlines()
# len_c=len(c)
# p_a=dict()
# ref_set=set()
# i=0
# while i<len_c:
#     if '#index' in c[i]:
#         index=c[i][7:-1]
#     if '#@' in c[i]:
#         authors=c[i][3:-1]
#         p_a.update({index:authors})
#         print(index)
#         print(p_a[index])
#         #x=input('enter a key')
#     i=i+1
# i=0
# st_time=int(input('Enter start Time:'))
# en_time=int(input('Enter End Time:'))
# while i<len_c:
#     if '#index' in c[i]:
#         index=c[i][7:-1]
#         print('Currently Seraching citation of paper index:')
#         print(index)
#         flag=0
#     if '#t' in c[i]:
#         try:
#         time=int(c[i][3:-1])
#     except:
#         time=2055
#     if '#%' in c[i] :
#         ref=c[i][3:-1]
#         print('Cited paper index:')
#         print(ref)
#         if time>=st_time and time<=en_time :
#             if index in p_a and ref in p_a:
#                 temp='@'+p_a[index]+'\n'+'->'+p_a[ref]+'\n'#formation of citation 
#                 of.write(temp)
#             if ref in p_a:              #Formation of collaboration of cited papers 
#                 if ref not in ref_set:
#                     ref_set.add(ref)
#                     authorlist=p_a[ref].split(";")
#                     len_au_list=len(authorlist)
#                     k=0
#                     while k<len_au_list:
#                         l=0
#                     while l<len_au_list:
#                             if k!=l:
#                                 colla=authorlist[k]+'\t'+authorlist[l]+'\t'+'1'+'\n'
#                                 of1.write(colla)
#                                 print('Citation updated')
#                             l=l+1
#                         k=k+1
#     i=i+1
# #collaboration development of all publication during time frame
# i=0
# while i<len_c:
#     if '#index' in c[i]:
#         index=c[i][7:-1]
#         print('Currently Seraching collaboration of paper index:')
#         print(index)
#     if '#t' in c[i]:
#     try:
#         time=int(c[i][3:-1])
#     except:
#         time=2055
#         if time>=st_time and time<=en_time :
#             if index in p_a:
#                 authorlist=p_a[index].split(";")#in sub-domain data handling split it by ','
#                 len_au_list=len(authorlist)
#                 k=0
#                 while k<len_au_list:
#                     l=0
#                     while l<len_au_list:
#                         if k!=l:
#                             colla=authorlist[k]+'\t'+authorlist[l]+'\t'+'1'+'\n'
#                             of1.write(colla)
#                             print('Collaboration updated')
#                         l=l+1
#                     k=k+1
#     i=i+1
    
# fp.close()
# of.close()
# of1.close()