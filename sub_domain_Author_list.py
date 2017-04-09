fp=open('software_engineering.txt','r')
of=open('software_engineering_authors.txt','w')

c=fp.readlines()
len_c=len(c)
p_a=dict()
authorid=0
i=0
while i<len_c:
    if '#@' in c[i]:
        author=c[i][2:-1]
        if author[-1]=='\r':
            author=author[:-1]
        authorlist=author.split(",")
        len_au_list=len(authorlist)
        k=0
        while k<len_au_list:
            if p_a.has_key(authorlist[k])==False:
                authorid=authorid+1
                p_a.update({authorlist[k]:authorid})
            k=k+1
        #print(author)
        #print(p_a[author])
    i=i+1
dict_len=len(p_a)
print(p_a.items())
for a in p_a:
    temp='#index '+str(p_a[a])+'\n'+'#n '+a+'\n'
    print(temp)
    of.write(temp)    
fp.close()
of.close()
                
        
