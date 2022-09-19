import os

good=[]
mmm=input('enter mapmaker input file, eg mapmaker_lg1.txt: ')
nnn=input('enter the marker order file, eg final_lg1.txt: ')

for i in os.listdir(os.getcwd()):
    if 'double_recombination_' in i:
        good.append(i)

out=open('markers_recombination_events.txt','w')
db={}
for i in good:
    f=open(i)
    for line in f:
        break
    for line in f:
        x=line.strip('\n').strip().split('\t')
        if x[1] not in db.keys():
            db[x[1]]=1
        else:
            db[x[1]]+=1
    f.close()

for i in db.keys():
    out.write(i+'\t'+str(db[i])+'\n')
out.close()
out=open('dbEvents.txt','w')
for i in db.keys():
    out.write(i+'\t'+str(db[i])+'\n')
out.close()

m=int(input('enter double recombination events threshold, eg 12: '))
info={}
f=open(mmm)
count=0
for line in f:
    if '*M' in line:
        count+=1
        info[str(count)]='Tag_'+line.split('\t')[0][2:]
f.close()
f=open(nnn)
for line in f:
    x=line.strip('\n').strip().split(' ')
    break
f.close()
out=open(nnn,'w')
result=''
count=0
temp=[]
for i in x:
    if info[i] in db.keys():
        if db[info[i]]<m:
            result+=i+' '
            temp.append(i)
        else:
            count+=1
    else:
        result+=i+' '
        temp.append(i)
out.write(result)
out.close()
print('bad marker num: ', count)
out=open('group_for_ripple.txt','w')
count=0
a=[[1,130],[110,240],[210,340],[310,440],[410,540],[510,640],[610,740],[710,840],[810,940],[910,1040],[1010,1140],[1110,1240],[1210,1340],[1310,1440]]
for k in a:
    if k[1]<len(temp):
        count+=1
        result='subgroup'+str(count)+'='
        for l in range(k[0],k[1]+1):
            result+=x[l]+' '
        out.write(result.strip()+'\n')
##        print(result)
    elif k[0]<=len(temp) and k[1]>len(temp):
        count+=1
        result='subgroup'+str(count)+'='
        for l in range(k[0],len(temp)+1):
            try:
                result+=x[l]+' '
            except:
                print(result)
        out.write(result.strip()+'\n')
##        print(result)
out.close()

m=input('enter any key to exit')

