## Ver1.1: fix ln96 5 to n

mmm=input('enter SNP meta file: ')
f=open(mmm)
m=input('enter your report file name: ')
n=10
marker_order=[]
plant_order=[]
plant_info={}
SNP_info={}
for line in f:
    x=line.strip('\n').strip().split('\t')
    if '#CHROM' in line:
        for i in range(10,len(x)):
            plant_order.append(x[i])
            plant_info[x[i]]=[]
    else:
        SNP_info[x[0]]=[]
        marker_order.append(x[0])
        for i in range(10,len(x)):
            SNP_info[x[0]].append(x[i])
            plant_info[plant_order[i-10]].append(x[i])
f.close()
##for i in plant_order:
##    print(plant_info[i])
##    n=input('enter anything')
##    if n=='q':
##        break
##    else:
##        continue
new_order={}
new_marker=[]
f=open(m)
for line in f:
    if 'order' not in line:
        x=line.split('\t')
        new_marker.append(x[1])
f.close()
for i in plant_order:
    new_order[i]=[]

for i in new_marker:
    ind=marker_order.index(i)
    for j in new_order.keys():
        new_order[j].append(plant_info[j][ind])

outname3='double_recombination_'+m
out3=open(outname3,'w')
head='plant name\tTag\tBefore this loci\tThis loci\tAfter this loci\n'
out3.write(head)

for i in new_order.keys():
    x=new_order[i]
    start=x[0]
    temp_list=[x[0]]
    sub_list=[]
    for j in range(1,len(x)-1):
        if x[j] in ['H','C','D','-'] and start in ['H','C','D','-']:
            temp_list.append(x[j])
            start='H'
            add_end=1
        elif x[j] in ['A','D','-'] and start in ['A','D','-']:
            temp_list.append(x[j])
            start='A'
            add_end=1
        elif x[j] in ['B','C','-'] and start in ['B','C','-']:
            temp_list.append(x[j])
            start='B'
            add_end=1
        else:
            sub_list.append(temp_list)
            temp_list=[]
            start=x[j]
            temp_list.append(x[j])
            add_end=0 
    if add_end==1:
        sub_list.append(temp_list)
    for k in range(len(sub_list)):
        if len(sub_list[k])<n:
            loci=0
            for p in range(k):
                loci+=len(sub_list[p])
            if k==0:
                continue
            elif k==len(sub_list)-1:
                continue
            else:
                for b in sub_list[k-1]:
                    if b in ['A','B','H']:
                        before=b
                        break
                for c in range(loci+2,len(x)):
                    if x[c] in ['A','B','H']:
                        after=x[c]
                        break
                if before==after:
                    change_marker=new_marker[loci]
                    result=i+'\t'+change_marker+'\t'
                    for q in sub_list[k-1][-n:]:
                        result+=q
                    result+='\t'
                    for q in sub_list[k]:
                        result+=q
                    result+='\t'
                    for q in sub_list[k+1][:n]:
                        result+=q
                    result+='\n'
                    out3.write(result)
                    new_order[i][loci]=before
    
out3.close()
true_event={}
possible_event={}
true_name={}
possible_name={}
for i in new_marker:
    true_event[i]=[]
    possible_event[i]=[]
    true_name[i]=[]
    possible_name[i]=[]
    
for i in new_order.keys():
    plant_ind=plant_order.index(i)
    x=new_order[i]
    start=x[0]
    temp_list=[x[0]]
    sub_list=[]
    add_end=0
    for j in range(1,len(x)):
        if x[j] in ['H','C','D','-'] and start in ['H','C','D','-']:
            temp_list.append(x[j])
            start='H'
            add_end=1
        elif x[j] in ['A','D','-'] and start in ['A','D','-']:
            temp_list.append(x[j])
            start='A'
            add_end=1
        elif x[j] in ['B','C','-'] and start in ['B','C','-']:
            temp_list.append(x[j])
            start='B'
            add_end=1
        else:
            sub_list.append(temp_list)
            temp_list=[]
            start=x[j]
            temp_list.append(x[j])
            add_end=0
    if add_end==1:
        sub_list.append(temp_list)
##    print(temp_list)
    for v in sub_list:
        if v==[]:
            sub_list.remove([])
##    print(i)
##    print(sub_list)
##    kk=input('break')
    for k in range(1,len(sub_list)):
        if len(sub_list[k-1]) > (n-1) and len(sub_list[k])> (n-1):
            loci=0
            for l in range(k):
                loci+=len(sub_list[l])
##            print(i)
##            print(sub_list)
##            print(sub_list[k-1])
##            print(plant_ind)
##            print(plant_order)
##            print(plant_order[plant_ind])
##            print(loci)
##            print(new_marker[loci])
##            print(new_marker)
##            kk=input('break')
##            true_name[new_marker[loci]].append(i)
##            true_event[new_marker[loci]].append(plant_ind)
##            if i=='A00027F':
##                print(sub_list)
            z=sub_list[k-1][:]
            z.reverse()
            for o in range(len(z)):
                if z[o] in ['A','B','H']:
                    true_name[new_marker[loci-o-1]].append(i)
                    true_event[new_marker[loci-o-1]].append(plant_ind)
                    break
                else:
                    possible_event[new_marker[loci-o-1]].append(plant_ind)
                    possible_name[new_marker[loci-o-1]].append(i)
        else:
            continue
##for s in new_marker:
##    print(s, '\t', true_name[s])
head=' \t'
for i in plant_order:
    head+=i+'\t'
head+='\n'
outname='Recombination_'+m
outname2='Rawdata_'+m
out2=open(outname2,'w')
out2.write(head)
out=open(outname,'w')
out.write(head)
for i in new_marker:
    result=i+'\t'
    z=SNP_info[i][:]
    for j in true_event[i]:
        z[j]='!!'+z[j]
    for k in possible_event[i]:
        z[k]='!'+z[k]
    for l in z:
        result+=l+'\t'
    result+='\n'
    out.write(result)
out.close()
for j in new_marker:
    result=j+'\t'
    for i in SNP_info[j]:
        result+=i+'\t'
    result+='\n'
    out2.write(result)
out2.close()
out4name='tag_info_'+m
out4=open(out4name,'w')
head='Tag\tall samples\tTrue\tPossible\n'
out4.write(head)
for i in new_marker:
    if len(possible_name[i])>0 or len(true_name[i])>0:
        result=i+'\t'
        for j in possible_name[i]:
            result+=j+','
        for j in true_name[i]:
            result+=j+','
        result+='\t'
        for j in true_name[i]:
            result+=j+','
        result+='\t'
        for j in possible_name[i]:
            result+=j+','
        result+='\n'
        out4.write(result)
out4.close()
                
            
                
            
            
                
            
                

