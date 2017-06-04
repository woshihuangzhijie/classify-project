# -*- coding: utf-8 -*-
# Author: hungzhijie <1500012884@pku.edu.cn>
#Time: 2017-05
# Algorithms: IF-IDF 算法 和 K-邻近算法
import random
import re
import math
from nltk.stem import SnowballStemmer
from nltk.corpus import reuters
import numpy as np
#字母字符串
letter='abcdefghijklmnopqrstuvwxyz'
#语言为英语
stemmer = SnowballStemmer('english')
#词的权重列表
Weight = [8,5,1,2]
#训练文件总数
Sum=7059
#单词词频列表
List1={}
StopWordsList = []
with open('stopwords', 'r') as StopWordsFile:
    for line in StopWordsFile.readlines():
        line = line.strip('\n')
        line = stemmer.stem(line)
        if line not in StopWordsList:
            StopWordsList.append(line)
StopWordsFile.close()
    # print(StopWordsList)
'''记录每个在语料库中的单词，并生成每个单词出现的文档数目，将其导入word.txt'''
#记录出现过的单词,并记录次数
List=reuters.fileids()[3019:]
'''for i in range(len(List)):
    li = []
    fp=open(List[i],'r')
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
            if ch_j not in li:
                List1[ch_j] += 1
                li.append(ch_j)
    del li
    fp.close()
#将结果写入word.txt
f=open("words.txt",'w+',encoding='utf-8')
#print(List1)
for i in List1:
    f.write(i)
    f.write('  ')
    f.write(str(List1[i]))
    f.write('\n')
f.close()'''
#从words.txt文件中读取数据,计算出每个单词的逆文档频率
with open('words.txt','r') as f:
    for line in f.readlines():
        line=line.strip()
        line = line.strip('\n')
        temp=line.split('  ')
        #print(temp)
        List1.setdefault(temp[0],int(temp[1]))
f.close()
def low(str):
    return str.lower()
#print(List1)
    # print(len(List1))
class SimilarText:
    #生成stop words列表
    def __init__(self):
        self.StopWordsList=StopWordsList

    #提取文本特征向量
    def FileVector(self,input):
        # 计算IDF的值
        def LetterRate(str1):
            if str1 in List1:
                len1 =List1[str1]
            else:
                len1=0
            return math.log((Sum)/(len1+0.01))
        InputFile=open(input,'r',encoding='utf-8')
        # 查找文章的尾句
        index = 0
        #文章长度
        length=0
        lines = InputFile.readlines()
        while index >= (-len(lines)):
            index -= 1
            if len(lines[index].strip()) != 0:
                break
        #查找文章第一段
        FirstSeg=0
        while lines[FirstSeg][0]!=' ':
            FirstSeg+=1
        index1 = 0  # 文章当前行
        index2 = 0  # 文章当前行（除空行）
        InputFileVector ={}

        for line in lines:
            # print(line)
            index1 += 1
            # print(index1)
            line = line.lower()
            line = line.strip()
            words = line.split()
            length+=len(words)
            # print(words)
            # 去除文章中的空行
            if len(words) == 0:
                continue
            for w in words:
                if len(w) == 0:
                    words.pop()
            if len(words) == 0:
                continue
            index2 += 1
            # print(index2)
            for word in words:
                # 文章的题目出现的单词的权重
                if index2 == 1:
                    weight = Weight[0]
                # 文章开头的权重
                elif index2<FirstSeg:
                    weight = Weight[1]
                # 为文章结尾的权重
                elif (len(lines) + index) == index1:
                    weight = Weight[3]
                else:
                    weight = Weight[2]
                #print(word)
                if len(word) == 0:
                    continue
                #print(word)
                #去除单词头部和尾部的非字母部分
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
                #print(word)
                #if word.isalpha()==0:
                if re.search(r'[^a-z-]', word) != None:
                    continue
                sword = stemmer.stem(word)
                if sword not in self.StopWordsList:
                    if sword in InputFileVector:
                        InputFileVector[sword] += weight
                    else:
                        InputFileVector.setdefault(sword,weight)
        InputFile.close()
        #print(InputFileVectorKey)
        #print(InputFileVectorValue)
        #计算特征向量分量的IF-IDF值

        for i in InputFileVector:
            InputFileVector[i] /=length
            InputFileVector[i]*=LetterRate(i)
        #求出特征向量
        SortVector=[]
        SortVector=sorted(InputFileVector.items(),key=lambda x:x[1],reverse=True)[:8]
        #print(SortVector)
        return SortVector
    #计算向量距离
    def SimValue(self,Vector1,Vector2):
        #归一化处理
        Vector=[]
        for i in Vector1:
            Vector.append(i[0])
        for i in Vector2:
            if i[0] not in Vector:
                Vector.append(i[0])
        V1={}
        V2={}
        Vector1Value=[]
        Vector2Value=[]
        for i in Vector1:
            V1.setdefault(i[0],i[1])
        for i in Vector2:
            V2.setdefault(i[0],i[1])
        for i in Vector:
            if i in V1:
                Vector1Value.append(V1[i])
            else:
                Vector1Value.append(0)
        for i in Vector:
            if i in V2:
                Vector2Value.append(V2[i])
            else:
                Vector2Value.append(0)
        for  i in range(len(Vector)):
            Vector1Value[i]=(Vector1Value[i]-min(Vector1Value))/(max(Vector1Value)-min(Vector1Value)+0.01)
            Vector2Value[i] =(Vector2Value[i] - min(Vector2Value)) / (max(Vector2Value) - min(Vector2Value)+0.01)
        dis=0
        for i in range(len(Vector)):
            dis+=(Vector1Value[i]-Vector2Value[i])**2
        return dis
#Top =self.Martic(TopicKey)
if __name__ == "__main__":
    f = open("classword.txt", 'r')
    lines = f.readlines()
    Top=[]
    for line in lines:
        TopicWord = []
        line = line.strip()
        V = line.split(' ')
        for i in range(0,len(V),2):
            TopicWord.append((V[i],float(V[i+1])))
        Top.append(TopicWord)
    f.close()
    S =SimilarText()
    FileList = reuters.fileids()[3019:]
    TopicVector=[]
    Sum=7059
    for i in FileList:
        TopicVector.append(S.FileVector(i))
    #print(FileList)
    index=0
    TrueCount=0
    TestList=reuters.fileids()[:3018]
    Test=random.sample(TestList, 500)
    for TestItem in Test:#List[:200]:#[:3000]:#reuters.fileids('earn'):#
        print(TestItem)
        Topic = {}
        TestVector = S.FileVector(TestItem)
        #print(TestVector)
        dis=[]
        for i in range(len(Top)):
            dis.append((reuters.categories()[i],S.SimValue(TestVector, Top[i])))
        dis.sort(key=lambda x:x[1])
        for x in range(10):
            Topic.setdefault(dis[x][0],20-2*x)
        Dis={}
        for i in range(len(FileList)):
            Dis.setdefault(FileList[i], S.SimValue(TestVector,TopicVector[i]))
        # 距离测试点最近的k个点
        R = sorted(Dis.items(), key=lambda x: x[1])[:35]
        FileTuple, FileKey = zip(*R)
        dis=1
        for r in FileTuple:
            for x in reuters.categories(r):
                if x not in Topic:
                    Topic.setdefault(x, dis)
                else:
                    Topic[x] += 35-dis
            dis+=1
        result=sorted(Topic.items(), key=lambda x: x[1], reverse=True)[:1]
        print(result[0][0])
        flag=0
        for r in result:
            if r[0] in reuters.categories(TestItem):
                TrueCount+=1
                flag=1
                print('True')
                break
        index +=1
        if flag==0:
            print('False')
    print(TrueCount)