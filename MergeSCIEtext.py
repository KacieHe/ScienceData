import os, csv, time

DBNAME = 'sci2011'
FieldSplitWithSemiList = ['AU', 'AF', 'C1', 'CR']
Btime = time.time()

def formattxt(folderpath):
    pathlist = os.listdir(folderpath)

    # 读取每条记录的分隔符ER,使用换行+ER+两个换行作为最终使用的分隔符
    with open(folderpath + pathlist[0], 'r', encoding = 'utf-8') as testfile:
        splitcode = [x for x in testfile.readlines() if x[:2] == 'ER'][0]
        splitcode = "{0}{1}{2}".format(splitcode[-1], splitcode, splitcode[-1]) # splitcode = splitcode[-1] + splitcode + splitcode[-1]

    recordlistnew = []
    for p in pathlist:
        with open(folderpath + p, 'r', encoding ="utf-8")as f:
            recordlist = [x.split('\n') for x in f.read().split(splitcode)]
            #检查文件格式(开始的FN/VR,结尾的EF)
            if recordlist[0][0][1:3] == 'FN' and recordlist[0][1][:2] == 'VR' and recordlist[-1][0][:2] == 'EF':
                pass
            else:
                print('{0}{1}文件存在错误,请检查文件!'.format(folderpath, p))
                input()
            #整理recordlist
            recordlist[0] = recordlist[0][2:]
            recordlist = recordlist[:-1]

            for r in recordlist:
                rnew = []
                for l in r:
                    if l[0] != ' ':
                        rnew.append(l)
                    else:
                        if rnew[-1][:2] in FieldSplitWithSemiList:
                            rnew[-1] += '; ' + l.strip()
                        else:
                            rnew[-1] += ' ' + l.strip()
                rnew.append('DF ' + folderpath + p)
                recordlistnew.append(rnew) 
    return recordlistnew

def record2dict(l):
    dictlist = []
    for r in l:
        recordict = {}
        for s in r:
            recordict[s.split(' ', 1)[0]] = s.split(' ', 1)[1]
        dictlist.append(recordict)
    return dictlist


recordlist = formattxt(DBNAME + '/')
print(time.time() - Btime)
recorddictlist = record2dict(recordlist)

### MEDLINE UT号去重
##newrecorddictlist = []
##utlist = []
##no = 0
##for r in recorddictlist:
##    if r['UT'] not in utlist:
##        newrecorddictlist.append(r)
##        utlist.append(r['UT'])
##        no += 1
##        if no % 1000 == 0:
##            print('%s条记录已经去重完毕，总进度%s, 总用时%s' % (no, no/113771, time.time() - Btime))
##recorddictlist = newrecorddictlist
##utlist = [x['UT'] for x in recorddictlist]
##print(len(utlist))
##print(len(set(utlist)))
### END

print(time.time() - Btime)
keyset = set()
for k in recorddictlist:
    for kk in k:
        keyset.add(kk)
print(len(list(keyset)))
print(keyset)
print(time.time() - Btime)

FIELDNAME = list(keyset)

with open(DBNAME + '.csv', 'w', encoding = 'utf-8') as csvfile:
    fieldnames = FIELDNAME
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(recorddictlist)

## 转换编码，去除换行
with open(DBNAME + '.csv', 'r', encoding = 'utf-8') as f:
    l = f.readlines()
nl = []
##dl = []
for i in l[::2]:
    nl.append(i.encode('gbk', 'replace').decode('gbk', 'replace'))
##    if len(i) < 40000:
##        nl.append(i.encode('gbk', 'replace').decode('gbk', 'replace'))
##    else:
##        dl.append(i.encode('gbk', 'replace').decode('gbk', 'replace'))
##        

print('%s共有%s条数据' % (DBNAME, len(nl)))

with open(DBNAME + '-gbk.csv', 'w', encoding = 'gbk') as f:
    f.writelines(nl)
##with open(DBNAME + '-gbk-add.csv', 'w', encoding = 'gbk') as f:
##    f.writelines(dl)
