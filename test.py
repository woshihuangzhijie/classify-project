# -*- coding: utf-8 -*-
from nltk.corpus import reuters
import text
import matplotlib.pyplot as plt
fp=open("cats.txt",'r')
lines=fp.readlines()
FileTopic=[]
for line in lines:
    line=line.strip()
    V=line.split(' ')
    FileTopic.append(V)
fp.close()
#print(FileTopic)
#print(reuters.categories('test/14826'))
f = open("classword.txt", 'r')
lines = f.readlines()
Top=[]
for line in lines:
    TopicWord = []
    line = line.strip()
    V = line.split(' ')
    TopicWord.append(V)
    Top.append(TopicWord)
f.close()
S =text.SimilarText()
FileList = reuters.fileids()[3019:]
TopicVector=[]
Sum=7059
for i in FileList:
    TopicVector.append(S.FileVector(i))
    #print(FileList)

while True:
    # TestList=reuters.fileids()[:3018]
    # Test=random.sample(TestList, 1)
    print("please enter your file name for test")
    string=input()
    TestItem = 'test/'+string
    if TestItem not in reuters.fileids():
        print('your file name does not exist')
        continue
    print(TestItem)
    Topic = {}
    TestVector = S.FileVector(TestItem)

    # print(TestVector)
    for i in range(len(Top)):
        for vector in TestVector:
            if vector in Top[i]:
                t = Top[i].index(vector)
                Topic.setdefault(reuters.categories[i], 10 - t)
    Dis = {}
    for i in range(len(FileList)):
        Dis.setdefault(FileList[i], S.SimValue(TestVector, TopicVector[i]))
    # 距离测试点最近的k个点
    R = sorted(Dis.items(), key=lambda x: x[1])[:20]
    FileTuple, FileKey = zip(*R)
    dis = 1
    for r in FileTuple:
        for x in reuters.categories(r):
            if x not in Topic:
                Topic.setdefault(x, dis)
            else:
                Topic[x] += 20 - dis
        dis += 1
    result = sorted(Topic.items(), key=lambda x: x[1], reverse=True)[:1]#[:2]
    '''if len(result) > 1:
        if (result[1][1] / result[0][1] < 0.6)
            result = result[:1]
    if len(result)>1:
        print(result[0][0],result[1][0])
    else:'''
    print(result[0][0])
    flag=0
    for r in result:
        if r[0] in reuters.categories(TestItem):
            print('True')
            flag=1
            break
    if flag==0:
        print('False')
