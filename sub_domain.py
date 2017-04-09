fp=open('AMiner-Paper.txt','r')#,encoding='utf-8')
of=open('Database.txt','w')#,encoding='utf-8')
c=fp.readlines()
len_c=len(c)
i=0
while i<len_c:
    if '#index' in c[i]:
        index=c[i][:-1]
    if '#*' in c[i]:
        title=c[i][:-1]
    if '#@' in c[i]:
        author=c[i][:-1]
    if '#o' in c[i]:
        affiliation=c[i][:-1]
    if '#t' in c[i]:
        time=c[i][:-1]
    if '#c' in c[i]:
        confer=c[i][3:-1]
        if 'Database' in confer or 'Databases' in confer or 'databases' in confer or 'database' in confer :
            buff=index+'\n'+title+'\n'+author+'\n'+affiliation+'\n'+time+'\n'+'#c '+confer+'\n'
            of.write(buff)
    if '#%' in c[i]:
        if 'Database' in confer or 'Databases' in confer or 'databases' in confer or 'database' in confer :
            of.write(c[i])
    i=i+1
fp.close()
of.close()
