of=open('citation_Database.txt','w')
of1=open('errFile_Database.txt','w')
Err_aut=set()
of2=open('collaboration_Database.txt','w')

fp=open('collaboration_author_Database.txt','r')#,encoding='utf-8')
b=fp.readlines()
len_b=len(b)
fp1=open('Paper_citation_network_Database.txt','r')#,encoding='utf-8')
c=fp1.readlines()
len_c=len(c)
fp2=open('AMiner-Author.txt','r')#,encoding='utf-8')
d=fp2.readlines()
len_d=len(d)
aut=dict()
i=0
while i<len_d:
    if '#index' in d[i]:
        index=d[i][7:-1]
    if '#n' in d[i]:
        author=d[i][3:-1]
        aut.update({author:index})
        #print(author)
        #print(aut[author])
    i=i+1

# Updating Collaboration.txt
x=0
while x<len_b:
    temp=''
    colla_author=b[x][0:-1]
    colla_author_list=colla_author.split("\t")
    if colla_author_list[0] in aut:
        temp=temp+aut[colla_author_list[0]]+'\t'
    if colla_author_list[1] in aut:
        temp=temp+aut[colla_author_list[1]]+'\t'+colla_author_list[2]+'\n'
    if colla_author_list[0] not in aut or colla_author_list[1] not in aut:
        temp=''
    else:
        of2.write(temp)
    x=x+1
# Updating citation Author names are replaced by Author index
j=0
while j<len_c:
    if '@' in c[j]:
        citing_authors=c[j][1:-1]
        citing_list=citing_authors.split(";")#In sub-domain code data is ',' seperated
        print(citing_list)
        k=0
        temp=''
        while k<len(citing_list):
            if citing_list[k] in aut:
                temp=temp+ '@' + aut[citing_list[k]]
            else:
                if citing_list[k] not in Err_aut:
		    Err_aut.add(citing_list[k])
                    of1.write(citing_list[k])
                    of1.write('\n')   
            k=k+1
        #print('Finished Citing List')
        if temp!='':
            temp=temp+'\n'
            #of.write(temp)
    if '->' in c[j] :
        cited_authors=c[j][2:-1]
        cited_list=cited_authors.split(";")#In sub-domain code data is ',' seperated
        print(cited_list)
        l=0
        #temp=''
        flag=0
        while l<len(cited_list):
            if cited_list[l] in aut and temp!='':
                flag=1
                temp=temp+'->'+aut[cited_list[l]]
            else:
                if cited_list[l] not in Err_aut:
		    Err_aut.add(cited_list[l])
                    of1.write(cited_list[l])
                    of1.write('\n') 
            l=l+1
        #print('Finished Cited List')
        if temp!='' and flag==1:
            temp=temp+'\n'
            of.write(temp)
    j=j+1
fp.close
fp1.close()
fp2.close()
of.close()
of1.close()
of2.close()
