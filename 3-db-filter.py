mmm=input('enter mapmaker input file, eg mapmaker_lg2.txt: ')
nnn=input('enter report file, eg report_lg2.txt: ')
zzz=input('enter double recombination report file, eg double_recombination_report_lg2.txt: ')
ppp=float(input('enter step size (cM), eg 1.5: '))
f=open(mmm)
out1=open('logfile_'+mmm,'w')
##out2=open('processed_mapmaker_lg1.txt','w')
info={}
info2={}
count=0
db={}
for line in f:
    if 'M' in line:
        count+=1
        tag='Tag_'+line.split('\t')[0][2:]
##        out2.write(geno[tag])
        db[tag]=0
        info[str(count)]=tag
        info2[tag]=str(count)
f.close()
f=open(zzz)
for line in f:
    break
for line in f:
    x=line.strip('\n').strip().split('\t')
    db[x[1]]+=1
f.close()
f=open(nnn)
for line in f:
    break
start=0
temp=[]
final=[]
for line in f:
    x=line.strip('\n').strip().split('\t')
    if float(x[2])>start:
        start=float(x[2])+ppp
        final.append(temp)
        temp=[x[1]]
    else:
        temp.append(x[1])
if final[-1]!=temp:
    final.append(temp)
##print(len(final))
result='pd '+mmm+'\nseq '
count=0
for i in final:
    score=300
    tag='tag'
    for j in i:
        if db[j]<score:
            score=db[j]
            tag=j
    result+=info2[j]+' '
    result1=tag+'\t'
    for j in i:
        result1+=j+'\t'
    out1.write(result1.strip('\t')+'\n')
    count+=1
print(count)

out=open('selectedFrame_'+mmm,'w')
out.write(result+'\norder\nq\ny\n')
out.close()
out1.close()
m=input('press any key to exit')
