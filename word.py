# -*- coding: utf-8 -*-
from nltk.corpus import reuters
import re
from nltk.stem import SnowballStemmer
letter = 'abcdefghijklmnopqrstuvwxyz'
stemmer = SnowballStemmer('english')
StopWordsList = []
with open('stopwords', 'r') as StopWordsFile:
    for line in StopWordsFile.readlines():
        line = line.strip('\n')
        line = stemmer.stem(line)
        if line not in StopWordsList:
            StopWordsList.append(line)
StopWordsFile.close()
    # print(StopWordsList)
#计算训练集中每类文章出现次数
FileSum=[]
for cate in reuters.categories():
    CateSum=0
    for file in reuters.fileids(cate):
        if file in reuters.fileids()[3019:]:
            CateSum+=1
    FileSum.append(CateSum)

#记录出现过的单词,并记录次数
List=reuters.categories()
ClassList=[]
for i in range(len(List)):
    List1 = {}
    #计算每一类文档的特征词语和词频
    for j in reuters.fileids(List[i]):
        if j in reuters.fileids()[3019:]:
            fp=open(j,'r')
            for line in fp.readlines():
                line = line.lower()
                line = line.strip()
                words = line.split()
                for word in words:
                    if len(word) == 0:
                        continue
                    while word[-1] not in letter:
                        word = word[0:-1]
                        if len(word) == 0:
                            break
                    if len(word) == 0:
                        continue
                    while word[0] not in letter:
                        word = word[1:]
                        if len(word) == 0:
                            break
                    if len(word) == 0:
                        continue
                    if re.search(r'[^a-z-\']', word) != None:
                        continue
                    ch_j = stemmer.stem(word)
                    if ch_j in StopWordsList:
                        continue
                    if ch_j not in List1:
                        List1.setdefault(ch_j, 1)
                    else:
                        List1[ch_j] += 1
            fp.close()
    sortList1=sorted(List1.items(),key=lambda x:x[1],reverse=True)[:100]
    sortList2=[]
    for voc in sortList1:
        sortList2.append((voc[0],voc[1]/FileSum[i]))
    print(sortList2)
    List1.clear()
    ClassList.append(sortList2)
#将结果写入classword.txt
f=open("classword.txt",'w+',encoding='utf-8')
#print(List1)
for i in ClassList:
    for j in i:
        f.write(j[0])
        f.write(' ')
        f.write(str(j[1]))
        f.write(' ')
    f.write('\n')
f.close()

