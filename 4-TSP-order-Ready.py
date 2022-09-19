def score(x):
    if x[0] in ['A','B'] and x[1] in ['A','B']:
        return 2
    elif x[0] in ['A','H'] and x[1] in ['A','H']:
        return 1
    elif x[0] in ['B','H'] and x[1] in ['B','H']:
        return 1
    elif x[0] in ['B','C'] and x[1] in ['B','C']:
        return 0
    elif x[0] in ['B','D'] and x[1] in ['B','D']:
        return 0
    elif x[0] in ['A','C'] and x[1] in ['A','C']:
        return 0
    elif x[0] in ['A','D'] and x[1] in ['A','D']:
        return 0
    elif x[0] in ['C','D','H'] and x[1] in ['C','D','H']:
        return 0

inputfile=input('enter mapmaker input file name, eg, mapmaker_lg1.txt: ')
outputfile=input('enter mapmaker out file name, eg, final_lg1.txt: ')

info={}
f=open(inputfile)
count=0
pos={}
for line in f:
    if '*M' in line:
        count+=1
        x=line.strip('\n').strip().split('\t')
        pos[str(count)]='Tag_'+x[0][2:]
        result=[]
        for i in range(1,len(x)):
            result.append(x[i])
        info['Tag_'+x[0][2:]]=result
f.close()

out=open('Marker-distanceVSframework-cM.txt','w')
f=open('frame-order.txt')
frame=[]
group={}
for line in f:
    x=line.strip('\n').strip().split(' ')
    if '=' in line:
        x=line.strip('\n').strip().split('=')[1].strip().split(' ')
    else:
        x=line.strip('\n').strip().split(' ')
    for i in x:
        if i!='':
            frame.append(pos[i])
            group[pos[i]]=[]
f.close()
head='Marker\t'
for i in frame:
    head+=i+'\t'
out.write(head.strip('\t')+'\n')
final={}
for i in info.keys():
    final[i]={}
bad=0
for i in info.keys():
    if i not in frame:
        judge=5000
        temp=[]
        result=i+'\t'
        for j in frame:
            miss=0
            count=0
            for k in range(len(info[i])):
                if '-' not in [info[i][k],info[j][k]]:
                    count+=1
                if info[i][k]!=info[j][k]:
                    if '-' not in [info[i][k],info[j][k]]:
                        x=score([info[i][k],info[j][k]])
                        miss+=x
            try:
                final[i][j]=miss/(count*2)
                result+=str(miss/(count*2))+'\t'
            except:
                print(i,info[i],j,info[j])
            if miss<judge:
                judge=miss
                temp=[j]
            elif miss==judge:
                temp.append(j)
        out.write(result.strip('\t')+'\n')
        if len(temp)==1:
            if temp[0]!=i:
                group[temp[0]].append(i)
        elif len(temp)>1:
            group[temp[0]].append(i)
f.close()
out.close()
out=open('frame-distance-cM.txt','w')
out.write(head.strip('\t')+'\n')
for i in frame:
    result=i+'\t'
    for j in frame:
        miss=0
        count=0
        for k in range(len(info[i])):
            if '-' not in [info[i][k],info[j][k]]:
                count+=1
            if info[i][k]!=info[j][k]:
                if '-' not in [info[i][k],info[j][k]]:
                    x=score([info[i][k],info[j][k]])
                    miss+=x
                    count+=1
        try:
            final[i][j]=miss/(count*2)
            result+=str(miss/(count*2))+'\t'
        except:
            print(i,info[i],j,info[j])
    out.write(result.strip('\t')+'\n')
out.close()
out=open('Marker-groupInfo-cM.txt','w')
for i in frame:
    result=i+'\t'
    for j in group[i]:
        result+=j+'\t'
    out.write(result.strip('\t')+'\n')
out.close()

f=open('frame-distance-cM.txt')
frame_dis={}
frame=[]
for line in f:
    x=line.strip('\n').strip().split('\t')
    for i in range(1,len(x)):
        frame.append(x[i])
        frame_dis[x[i]]={}
    break

for line in f:
    x=line.strip('\n').strip().split('\t')
    for i in range(1,len(x)):
        frame_dis[x[0]][frame[i-1]]=float(x[i])
f.close()
##print(frame)
f=open('Marker-distanceVSframework-cM.txt')
marker_dis={}
marker_triple={}

for line in f:
    break

for line in f:
    x=line.strip('\n').strip().split('\t')
    marker_dis[x[0]]={}
    marker_triple[x[0]]={}
    for i in range(1,len(x)):
        marker_dis[x[0]][frame[i-1]]=float(x[i])
    for i in range(1,len(x)-1):
        marker_triple[x[0]][frame[i-1]]=float(x[i])+float(x[i+1])
f.close()
print(len(marker_triple.keys()))
group={}
for i in frame:
    group[i]=[]
for i in marker_dis.keys():
    temp=[]
    tag='tag'
    dis=100000
    for j in frame:
        if marker_dis[i][j]<dis:
            dis=marker_dis[i][j]
            temp=[j]
        elif marker_dis[i][j]==dis:
            temp.append(j)
    if len(temp)==1:
        group[temp[0]].append(i)

used={}
group2={}
for i in range(len(frame)-1):
    group2[frame[i]]=[]

for i in marker_triple.keys():
    temp=[]
    tag='tag'
    dis=100000
    for j in range(len(frame)-1):
        if marker_triple[i][frame[j]]<dis:
            dis=marker_triple[i][frame[j]]
            temp=[frame[j]]
        elif marker_triple[i][frame[j]]==dis:
            temp.append(frame[j])
    if len(temp)==1:
        group2[temp[0]].append(i)
    else:
        print(i,temp)
##print(len(marker_triple.keys()))
count=0
for i in group2.keys():
    count+=1+len(group2[i])
print(count)
order=[[]]
for i in frame:
    order.append([])
for i in group[frame[0]]:
    if len(group[frame[0]])>0:
        for j in group[frame[0]]:
            if marker_dis[j][frame[1]]>frame_dis[frame[0]][frame[1]]:
                order[0].append(j)
                used[j]=1

for i in group[frame[-1]]:
    if len(group[frame[-1]])>0:
        for j in group[frame[-1]]:
            if marker_dis[j][frame[-2]]>frame_dis[frame[-1]][frame[-2]]:
                order[-1].append(j)
                used[j]=1
for i in range(len(frame)-1):
    if len(group2[frame[i]])>0:
        for j in group2[frame[i]]:
            if j not in used.keys():
                order[i].append(j)
##print(len(order),len(frame))
count=0
for i in order:
    count+=1+len(i)
##print(order)

final=[]
if len(order[0])<2:
    final.append(order[0])
else:
    temp={}
    temp['pos']=[]
    for j in order[0]:
        score=marker_dis[j][frame[0]]
        if str(score) not in temp.keys():
            temp['pos'].append(score)
            temp[str(score)]=[]
        temp[str(score)].append(j)
    temp['pos'].sort()
    temp2=[]
    for j in temp['pos'][::-1]:
        for k in temp[str(j)]:
            temp2.append(k)
    final.append(temp2)

for i in range(1,len(frame)-1):
    if len(order[i])<2:
        final.append(order[i])
    else:
        temp={}
        temp['pos']=[]
        for j in order[i]:
            score=marker_dis[j][frame[i]]
            if str(score) not in temp.keys():
                temp['pos'].append(score)
                temp[str(score)]=[]
            temp[str(score)].append(j)
        temp['pos'].sort()
##        print(temp)
        temp2=[]
        for j in temp['pos'][::-1]:
            for k in temp[str(j)]:
                temp2.append(k)
        final.append(temp2)

if len(order[-1])<2:
    final.append(order[-1])
else:
    temp={}
    temp['pos']=[]
    for j in order[-1]:
        score=marker_dis[j][frame[-1]]
        if str(score) not in temp.keys():
            temp['pos'].append(score)
            temp[str(score)]=[]
        temp[str(score)].append(j)
    temp['pos'].sort()
    temp2=[]
    for j in temp['pos']:
        for k in temp[str(j)]:
            temp2.append(k)
    final.append(temp2)
##print(len(order),len(final))
##count=0
##for i in final:
##    count+=1+len(i)
##print(count)
final_order=[]
used={}
for i in range(len(frame)):
    if len(final[i])>0:
        for j in final[i]:
            if j not in used.keys():
                used[j]=1
                final_order.append(j)
            else:
                print(j)
    if frame[i] not in used.keys():
        final_order.append(frame[i])
        used[frame[i]]=1
    else:
        print(frame[i])
if len(final[-1])>0:
    for j in final[-1]:
        if j not in used.keys():
            final_order.append(j)
            used[j]=1
        else:
            print(j)
##print(len(final_order))
##print(order)


count=0
info={}
f=open(inputfile)
for line in f:
    if '*M' in line:
        count+=1
        info['Tag_'+line.split('\t')[0][2:]]=str(count)
f.close()
##print(len(final_order))
result=''
for i in final_order:
    result+=info[i]+' '
out=open(outputfile,'w')
out.write(result)
out.close()



        
    
                    
                
        
    
    
