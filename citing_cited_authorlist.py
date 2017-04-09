fp=open('Database.txt','r')
of=open('Paper_citation_network_Database.txt','w')
of1=open('collaboration_author_Database.txt','w')
c=fp.readlines()
len_c=len(c)
p_a=dict()
ref_set=set()
i=0
while i<len_c:
    if '#index' in c[i]:
        index=c[i][7:-1]
    if '#@' in c[i]:
        authors=c[i][3:-1]
        p_a.update({index:authors})
        print(index)
        print(p_a[index])
        #x=input('enter a key')
    i=i+1
i=0
st_time=int(input('Enter start Time:'))
en_time=int(input('Enter End Time:'))
while i<len_c:
    if '#index' in c[i]:
        index=c[i][7:-1]
        print('Currently Seraching citation of paper index:')
        print(index)
        flag=0
    if '#t' in c[i]:
        try:
	    time=int(c[i][3:-1])
	except:
	    time=2055
    if '#%' in c[i] :
        ref=c[i][3:-1]
        print('Cited paper index:')
        print(ref)
        if time>=st_time and time<=en_time :
            if index in p_a and ref in p_a:
            	temp='@'+p_a[index]+'\n'+'->'+p_a[ref]+'\n'#formation of citation 
            	of.write(temp)
            if ref in p_a:				#Formation of collaboration of cited papers 
            	if ref not in ref_set:
                    ref_set.add(ref)
                    authorlist=p_a[ref].split(";")
                    len_au_list=len(authorlist)
                    k=0
                    while k<len_au_list:
                    	l=0
                   	while l<len_au_list:
                            if k!=l:
                            	colla=authorlist[k]+'\t'+authorlist[l]+'\t'+'1'+'\n'
                            	of1.write(colla)
                            	print('Citation updated')
                            l=l+1
                    	k=k+1
    i=i+1
#collaboration development of all publication during time frame
i=0
while i<len_c:
    if '#index' in c[i]:
        index=c[i][7:-1]
        print('Currently Seraching collaboration of paper index:')
        print(index)
    if '#t' in c[i]:
	try:
		time=int(c[i][3:-1])
	except:
		time=2055
        if time>=st_time and time<=en_time :
            if index in p_a:
                authorlist=p_a[index].split(";")#in sub-domain data handling split it by ','
                len_au_list=len(authorlist)
                k=0
                while k<len_au_list:
                    l=0
                    while l<len_au_list:
                        if k!=l:
                            colla=authorlist[k]+'\t'+authorlist[l]+'\t'+'1'+'\n'
                            of1.write(colla)
                            print('Collaboration updated')
                        l=l+1
                    k=k+1
    i=i+1
    
fp.close()
of.close()
of1.close()
                
        
