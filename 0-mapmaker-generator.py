m=input('enter population type: f2 intercross, f2 backcross, f3 self, ri self, ri sib: ')
n=input('enter the progeny number: ')
x1=input('enter SNP meta file name: ')
x2=input('enter mstmap marker order: ')
x3=input('enter output file name (format: mapmaker_lg*.txt: ')
f=open(x1)
info={}

for line in f:
    break

for line in f:
    x=line.strip('\n').strip().split('\t')
    result="*M"+x[0].split('_')[1]+'\t'
    for i in range(10,len(x)):
        if m in ['f2 intercross', 'f3 self']:
            result+=x[i]+'\t'
        elif m in ['ri self', 'ri sib']:
            if x[i] in ['A','B']:
                result+=x[i]+'\t'
            else:
                result+='-\t'
        else:
            if x[i] in ['A','H']:
                result+=x[i]+'\t'
            else:
                result+='-\t'
    info[x[0]]=result.strip('\t')+'\n'
f.close()

temp=[]

f=open(x2)
for line in f:
    if 'Tag' in line:
        temp.append(line.split('\t')[0])
f.close()
out=open('final_'+x3.split('_')[1],'w')
result=''
for i in range(len(temp)):
    result+=str(i+1)+' '
out.write(result)
out.close()

out=open(x3,'w')
out.write('data type '+m+'\n'+n+' '+str(len(temp))+' 0\n')
for i in temp:
    out.write(info[i])
out.close()

y=input('press any key to exit')
                
    
