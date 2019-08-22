import  numpy as np
import math

word2id,id2word = {},{}
tag2id,id2tag = {},{}

for line in open("traindata.txt"):
    word,tag = line.split("/")
    tag = tag.rstrip()
    if not word in word2id:
        word2id[word]=len(word2id)
        id2word[len(id2word)]=word

    if not tag in tag2id:
        tag2id[tag]=len(tag2id)
        id2tag[len(id2tag)]=tag

M = len(word2id)  # M为单词数量
N = len(tag2id)   # N为词性数量

#发射矩阵
A = np.zeros((N,M))
#状态转移矩阵
B = np.zeros((N,N))
#初始矩阵
Pi = np.zeros(N)

word_list = []
tag_list = []
word,tag,temp_word,temp_tag = '','','',''
for line in open("traindata.txt"):
    temp_word, temp_tag = line.split("/")
    temp_tag = temp_tag.rstrip()

    word_id = word2id[temp_word]
    tag_id = tag2id[temp_tag]
    A[tag_id][word_id] += 1
    if(word == '.' or word == ''):
        Pi[tag_id] += 1
    if not tag == '':
        B[tag2id[tag]][tag_id] += 1
    word = temp_word
    tag = temp_tag

for i in range(N):
    A[i] = A[i]/sum(A[i])
    B[i] = B[i]/sum(B[i])

Pi = Pi/sum(Pi)


def log(v):
    if v == 0:
        return np.log(0.0000001)
    return np.log(v)

def tag_analyse(sentence):
    id_list = []
    path_list = []
    tag_path = []
    for w in sentence.split(" "):
        id_list.append(word2id[w])
    print(id_list)
    dp = np.zeros((N, len(id_list)))
    path = np.zeros((N, len(id_list)))
    for i in range(N):
        #print(Pi[i],A[i][id_list[0]])
        dp[i][0] = log(Pi[i]+A[i][id_list[0]])
        #print(dp[i][0])

    for row in range(1,len(id_list)):
        for col in range(N):
            #max = dp[col][row-1]+log(A[0][id_list[row]])+log(B[0][col])
            max = -99999
            for i in range(N):
                tmax = dp[i][row-1]+log(A[i][id_list[row]])+log(B[i][col])
                #print(dp[i][row - 1],"---" , log(A[i][id_list[row]]) ,"----", log(B[i][col]),"----",tmax)
                if tmax > max:
                    max = tmax
                    dp[col][row]=max
                    path[col][row] = i

    ind = -1
    min_index = np.argmin(dp[:][ind])
    print(min_index)
    while(len(path_list)<len(id_list)-1):
        ind -= 1
        path_list.insert(0,min_index)
        min_index = path[min_index][ind]
        min_index = int(min_index)
    path_list.insert(0, min_index)
    #print(path_list)
    for p in path_list:
        tag_path.append(id2tag[p])
    print("对应的标签为：",tag_path)
    return tag_path


tag_analyse("keep new with rival")


