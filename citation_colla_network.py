import networkx as nx
g=nx.DiGraph()   
fp=open('citation_Database.txt','r')
c = fp.readlines()
len_c=len(c)
k=0
self_cite=0
while k<len_c:
    #Finding Citing Author List
    if '@' in c[k]:
        citing=c[k][1:-1]
        citing_list=citing.split("@")
        citing_set=set(citing_list)# Making Citing authors set

    #Finding Cited Author List
    if '->' in c[k]:
        cited=c[k][2:-1]
        cited_list=cited.split("->")
        cited_set=set(cited_list)# Making cited Authors set
        
	#Developing Citation Network
        #Removing Self Citation
        if len(citing_set.intersection(cited_set))== 0:
            for i in range(0,len(citing_list)):
                for j in range(0,len(cited_list)):
                    if g.has_edge(citing_list[i],cited_list[j]):
                        g[citing_list[i]][cited_list[j]]['citation']=g[citing_list[i]][cited_list[j]]['citation']+1
                        g[citing_list[i]][cited_list[j]]['total']=0
                        g[citing_list[i]][cited_list[j]]['total']=g[citing_list[i]][cited_list[j]]['total']+g[citing_list[i]][cited_list[j]]['citation']*0.4
                        print('Citation score Updated')
                        #input('Press Any Key')
                    else:
                        if citing_list[i]=='' or cited_list[j]=='':
                            print('discard Edge')
                            #input('press any key')
                        else:
                            g.add_edge(citing_list[i],cited_list[j],citation=1,colla=0,total=0)
                            g[citing_list[i]][cited_list[j]]['total']=g[citing_list[i]][cited_list[j]]['total']+g[citing_list[i]][cited_list[j]]['citation']*0.4
		            #input('New edge created')
        else:
	    self_cite=self_cite+1
            print('Self Citation')
            #input('press any key')
    k=k+1
#print(g.edges(data=True))
print('Citation Network updated')
print('Total self citation occured:',self_cite)
#x=input("Press any key")
fp.close()

#development of collaboration network
# Update this section
fp1=open('collaboration_Database.txt','r')
d=fp1.readlines()
len_d=len(d)
l=0
while l<len_d:
    collaboration=d[l][0:-1]
    coll_list=collaboration.split("\t")
    if g.has_edge(coll_list[0],coll_list[1]):
        g[coll_list[0]][coll_list[1]]['colla']=g[coll_list[0]][coll_list[1]]['colla']+1
        g[coll_list[0]][coll_list[1]]['total']=0
        g[coll_list[0]][coll_list[1]]['total']=g[coll_list[0]][coll_list[1]]['total']+g[coll_list[0]][coll_list[1]]['colla']*0.6
        g[coll_list[0]][coll_list[1]]['total']=g[coll_list[0]][coll_list[1]]['total']+g[coll_list[0]][coll_list[1]]['citation']*0.4
        print('Collaboration score Updated')
    else:
        g.add_edge(coll_list[0],coll_list[1],citation=0,colla=1,total=0)
	#print(g.node[coll_list[0]]['trust'])
        g[coll_list[0]][coll_list[1]]['total']=g[coll_list[0]][coll_list[1]]['total']+g[coll_list[0]][coll_list[1]]['colla']*0.6
    l=l+1
    #input("Press any key")
#print(g.edges(data=True))
print('collaboration Network updated')
#input("Press any key")
fp1.close()
nx.set_node_attributes(g, 'res_trust', 0.2)# Setting node attribute  trust= residual trust value
nx.set_node_attributes(g,'u_trust',0.2)
nx.set_node_attributes(g,'temp_trust',0)
nx.set_node_attributes(g,'citation',0)
#Normalizing total weight
w1=g.number_of_nodes()
node_list=g.nodes()
w=0
while w<w1:
    neighbor_list=g.neighbors(node_list[w])
    y=0
    len_neighbor_list=len(neighbor_list)
    tot=0
    while y<len_neighbor_list:
        tot=tot+ g[node_list[w]][neighbor_list[y]]['total']
        y=y+1
    y=0
    while y<len_neighbor_list:
        g[node_list[w]][neighbor_list[y]]['total']=g[node_list[w]][neighbor_list[y]]['total']/tot
        print(node_list[w],neighbor_list[y],g[node_list[w]][neighbor_list[y]]['total'])
        #k=input('press any key')
        y=y+1
    w=w+1

#Iteration to Update the all node trust value
w1=g.number_of_nodes()
node_list=g.nodes()
r=0
cite_flag=0
while r<2:
    w=0
    while w<w1:#LOOP for calculating for all nodes in the network
        neighbor_list=g.neighbors(node_list[w])
        y=0
        len_neighbor_list=len(neighbor_list)
        print('For Node:'+node_list[w])
        while y<len_neighbor_list:# LOOP for Neighbors of one node
            g.node[neighbor_list[y]]['temp_trust']=g.node[neighbor_list[y]]['temp_trust']+g[node_list[w]][neighbor_list[y]]['total']*g.node[node_list[w]]['u_trust']
            if cite_flag==0:# Calculating citation count of node
                g.node[neighbor_list[y]]['citation']=g.node[neighbor_list[y]]['citation']+g[node_list[w]][neighbor_list[y]]['citation']
            print(neighbor_list[y],g.node[neighbor_list[y]]['temp_trust'])
            print(neighbor_list[y],g.node[neighbor_list[y]]['citation'])  
            y=y+1
        w=w+1
    cite_flag=1
    w=0
    #print('Updating Universal Trust')
    while w<w1:#Updating temp trust to Universal Trust after calculating trust of all nodes in one iteration
        g.node[node_list[w]]['u_trust']=g.node[node_list[w]]['temp_trust']
        g.node[node_list[w]]['temp_trust']=0
        print(node_list[w],g.node[node_list[w]]['u_trust'])
        print(node_list[w],g.node[node_list[w]]['citation'])
        w=w+1
    r=r+1
w=0
buff=''
of=open('Trust_citation_Database.csv','w')
while w<w1:
    buff=buff+node_list[w]+'\t'+str(g.node[node_list[w]]['u_trust'])+'\t'+str(g.node[node_list[w]]['citation'])+'\n'
    of.write(buff)
    buff=''
    w=w+1
of.close()

