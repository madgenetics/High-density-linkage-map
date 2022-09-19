import subprocess
import os
good=[]
for i in os.listdir(os.getcwd()):
    if 'final_lg' in i:
        good.append(i)

for zzzz in good:
##    for iiii in range(1,10):
    m='mapmaker_'+zzzz.split('_')[1]
    n='SNP_loci.txt'
    lll=zzzz
    f=open(lll)
    for line in f:
        l=line.strip('\n')
        break
    f.close()

    all_info={}
    f=open(n)
    for line in f:
        x=line.strip('\n').strip().split('\t')
        all_info[x[0]]=[x[1],x[2]]
    f.close()

    mapmaker_list={}
    f=open(m)
    count=0
    for line in f:
        if '*' in line:
            count+=1
            x='Tag_'+line.split('\t')[0][2:]
            mapmaker_list[str(count)]=x
    f.close()
    outname='report_'+m.split('_')[1]
    out=open(outname,'w')
    x=l.strip('\n').strip().split(' ')

    length=len(x)
    group=[]
    subgroup=length//40
    remain=length%40
    if remain!=0:
        if subgroup==0:
            sub=[]
            for j in x:
                sub.append(j)
            group.append(sub)
        elif subgroup ==1:
            sub=[]
            for j in range(41):
                sub.append(x[j])
            group.append(sub)
            sub=[]
            for j in range(37, length):
                sub.append(x[j])
            group.append(sub)
        else:
            sub=[]
            for j in range(40):
                sub.append(x[j])
            group.append(sub)
            for t in range(1,subgroup):
                sub=[]
                for j in range((t*40-3), (t+1)*40):
                    sub.append(x[j])
                group.append(sub)
            sub=[]
            for j in range((subgroup*40-3),length):
                sub.append(x[j])
            group.append(sub)
    else:
        if subgroup==1:
            sub=[]
            for j in range(41):
                sub.append(x[j])
            group.append(sub)
        else:
            sub=[]
            for j in range(41):
                sub.append(x[j])
            group.append(sub)
            for t in range(1, subgroup):
                sub=[]
                for j in range((t*40-3),(t+1)*40):
                    sub.append(x[j])
                group.append(sub)
            sub=[]
            for j in range((subgroup*40-3),length):
                sub.append(x[j])
            group.append(sub)
    ##print(group)
    c1='prepare data '+m+'\n'
    for i in group:
        seq='seq '
        for j in i:
            seq+=j+' '
        seq+='\ncentimorgan kosambi\nerror detection on\nmap\n'
        c1+=seq
    c1+='q\ny\n'
    cmdfile='cmd_map_'+m
    out1=open(cmdfile,'w')
    out1.write(c1)
    out1.close()
    cmdout='map_'+m
    shellcmd='mapmaker<'+cmdfile+'>'+cmdout
    process=subprocess.Popen(shellcmd, shell=True)
    process.wait()
    f=open(cmdout)
    mapjudge=0
    marker_list=[]
    marker_info={}
    for line in f:
        if 'Markers' in line and 'Distance' in line:
            mapjudge=1
        elif 'log-likelihood' in line:
            mapjudge=0
        if mapjudge==1:
            if 'Markers' not in line:
                o=line.strip('\n').strip().split(' ')
                z=[]
                for i in o:
                    if i!='':
                        z.append(i)
                r='Tag_'+z[1][1:]
                if r not in marker_info.keys():
                    marker_list.append(r)
                if '---' not in line:
                    marker_info[r]=z[2]
                else:
                    marker_info[r]=0.0
    marker_info2={}
    marker_info2[marker_list[0]]=0.0
    ##print(marker_list)
    ##print(marker_info)
    for i in range(1,len(marker_list)):
    ##    print(marker_list[i])
        marker_info2[marker_list[i]]=marker_info2[marker_list[i-1]]+float(marker_info[marker_list[i-1]])
    ##for i in marker_list:
    ##    result=i+'\t'+str(round(marker_info2[i],1))
    ##    print(result)
                
                        
                        


    final_count=0
    ##print(mapmaker_list)
    ##print(x)
    result='order\tSNP_name\tgenotypic_score(cM)\tChro\tPOS\n'
    out.write(result)
    for i in marker_list:
    ##    print(i)
    ##    print(mapmaker_list[i])
    ##    print(str(round(marker_info2[mapmaker_list[i]],1)))
    ##    print(all_info[mapmaker_list[i]][0])
    ##    print(all_info[mapmaker_list[i]][1])
        final_count+=1
        result=str(final_count)+'\t'+i+'\t'+str(round(marker_info2[i],1))+'\t'+all_info[i][0]+'\t'+all_info[i][1]+'\n'
        out.write(result)
    out.close()

