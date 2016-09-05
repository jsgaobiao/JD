import os, sys
import pdb

f = open('result.txt')
fout = open('result_sorted.txt','w')
cnt = -1
a = []

for lines in f :
    line = lines.rstrip('\n')
    line = line.split('\t')
    line[2] = float(line[2])
    cnt += 1
    a.append(line)

a.sort(key = lambda x:x[2])

cnt = -1
for i in reversed(a) :
    ori_name = i[0]
    cnt += 1
    tmp = i[0].split('/')
    i[0] = tmp[2]
    i[0] = '%04d_%s' % (cnt, i[2])
    os.system('cp '+ori_name+' sorted_files/'+i[0])
    k = '\t'.join([str(j) for j in i])
    fout.write(k + '\n')

f.close()
fout.close()
