import os
import pdb
import numpy as np
f = open('result.txt')
#fout = open('output.txt','w')
totfile = 0
cnt = 0
corr = 0
err = [0, 0, 0]
pre = [0, 0, 0]
errto = [[0,0,0],[0,0,0],[0,0,0]]

for lines in f:
    totfile += 1
    line = lines.rstrip('\n')
    line = line.split('\t')
    cnt += 1
    num = [float(line[2]), float(line[3]), float(line[4])]
    index = np.argmax(num)
    if max(num[0], num[1], num[2]) == num[int(line[1])]:
        corr += 1
    else:
        err[int(line[1])] += 1
        errto[int(line[1])][index] += 1
    pre[index] += 1
    #os.system('cp '+line[0]+' tencent_fail/' + line[1] + '_' + str(index) + '_' + str(num[index]) + '.jpg')
print 'Accuracy : ' ,float(corr) / float(cnt)
print 'Error Check 0: ', float(errto[1][0] + errto[2][0]) / float(pre[0])
print 'Miss Check 0: ', float(err[0]) / float(totfile)
print '0 -> 1: ', errto[0][1]
print '0 -> 2: ', errto[0][2]
print ' '
print 'Error Check 1: ', float(errto[0][1] + errto[2][1]) / float(pre[1])
print 'Miss Check 1: ', float(err[1]) / float(800)
print '1 -> 0: ', errto[1][0]
print '1 -> 2: ', errto[1][2]
print ' '
print 'Error Check 2: ', float(errto[0][2] + errto[1][2]) / float(pre[2])
print 'Miss Check 2: ', float(err[2]) / float(800)
print '2 -> 0: ', errto[2][0]
print '2 -> 1: ', errto[2][1]
f.close()
#fout.close()
