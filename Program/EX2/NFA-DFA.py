
# coding: utf-8

# # 输入操作

# In[1]:

file_name1 = 'Table1'
file_name2 = 'DFA1'


# In[2]:

# 输入状态个数
N =int(input('请输入状态个数: '))

S = []
for i in range(N):
    S.append(int(i))

S


# In[3]:

# 输入状态转换表 s c e
'''
    s: 起始状态
    c: 转移字符
    e: 到达状态
'''
# M = int(input())
Table = []
path = './Data/'+file_name1+'.txt'
fin = open(path)
lines = fin.readlines()
for line in lines:
    Table.append([])
    Table[len(Table)-1] = line.rstrip().split(' ')

Table


# In[4]:

# 开始状态
B = input('请输入开始状态: ')
print('开始状态:', B)


# In[5]:

# 接受(结束)状态表
E = []
t = input('请输入接受状态: ')
E = t.split(' ')

print('接受状态:', E)


# ## 判断为NFA还是DFA

# In[6]:

def NFA_DFA(Table):
    isNFA = False
    for i in range(len(Table)):
        for j in range(len(Table)):
            if(i != j and Table[i][0]==Table[j][0] and Table[i][1]==Table[j][1] and Table[i][1]==Table[j][1] and Table[i][2]!=Table[j][2]):
                isNFA = True
                break
        if(isNFA==True):
            break

    if(isNFA):
        print("读入自动机输入文件为 NFA")
    else:
        print("读入自动机输入我呢件为 DFA")
    
    return isNFA
        
isNFA = NFA_DFA(Table)


# ### ε-closure闭包算法

# In[7]:

# ε-closure闭包算法
def Closure(a, T):
    b = a
    while 1:
        s = []
        for i in a:
            for j in range(len(T)):
                if(i==T[j][0] and T[j][1]=='~'):
                    s.append(T[j][2])
        if(len(s)==0):
            break;
        else:
            for i in s:
                b.append(i)
                a = s
    b = sorted(b)
    return b    


# ### Edge

# In[8]:

def Edge(a, c, T):
    s = []
    for i in a:
        for j in range(len(T)):
            if(i==T[j][0] and T[j][1]==c):
                s.append(T[j][2])
    s = sorted(s)
    return s


# # NFA=>DFA

# In[9]:

C = ['0', '1']

S1 = []
S2 = []
S1.append(Closure(['0'], Table))
S2.append(0)

while(S2.pop(len(S2)-1)==0):
    S2.append(0)
    for i in range(len(S1)):
        if(S2[i]==0):
            S2[i] = 1
            for c in C:
                s = Edge(S1[i], c, Table)
                print("Edge %c: %s" % (c,set(map(int,s))))  ###
                #if(s==[]):
                    #break
                s = Closure(s, Table)
                print("Closure %c: %s" % (c,set(map(int,s))))   ###
                #if(s==[]):
                    #break
                    
                flag = 0        # flag统计S1中是否有s集合
                for m in S1:
                    if(s==m):
                        flag = 1
                        break
                        
                if(flag==0 and s!=[]):    # 添加新出现的集合
                    S1.append(s)
                    S2.append(0)
                    

print('\n输出NFA构造的子集:')
for i in range(len(S1)):
    Set = set(map(int,S1[i]))
    print("%d: %s" % (i, Set))
print()


print('输出DFA:')
print('S', end = '\t')
for x in ['0','1','E']:
    print(x, end = '\t')
print('')

# 输出DFA
DFA = []
for i in range(len(S1)):
    DFA.append([]) ###
    
    DFA[i].append(i) ###
    print(i, end = '\t')
    for c in C:
        s = Edge(S1[i], c, Table)
        if(s==[]):
            DFA[i].append(s)
            print(s, end='\t')
            continue
        s = Closure(s, Table)
        if(s==[]):
            DFA[i].append(s)
            print(s, end='\t')
            continue
        for k in range(len(S1)):
            if(S1[k]==s):
                DFA[i].append(k)
                print(k, end='\t')
                break
                
    end = False
    for m in E:
        if m in S1[i]:
            end = True
    
    if(end==False):
        print(0)
    else:
        print(1)
    DFA[i].append(int(end))
    
DFA


# ### DFA表输出

# In[10]:

path = './Data/'+file_name2+'.txt'
fout = open(path, 'w')
for i in DFA:
    k = '\t'.join([str(j) for j in i])
    fout.write(k+"\n")
fout.close()


# In[11]:

T_in = []
path = './Data/'+file_name2+'.txt'
fin = open(path)
lines = fin.readlines()
for line in lines:
    T_in.append([])
    T_in[len(T_in)-1] = line.rstrip().split('\t')

fin.close()
T_in


# # DFA最小化

# ### 初始分割子集

# In[12]:

def InitSet(T_in):
    SET = [[],[]]
    for i in range(len(T_in)):
        if(int(T_in[i][3]) == 0):
            SET[0].append(int(T_in[i][0]))
        else:
            SET[1].append(int(T_in[i][0]))
    
    return SET


# ### 判断元素x是否在集合Set中

# In[13]:

def Find(Set, x):
    try:
        if(x != [] or x != ''):
            for i in range(len(Set)):
                 if(Set.index(x) != -1):
                    return True
        else:
            return False
    except:
        return False


# ### 判断是否等价

# In[14]:

def Equal(A, B):
    flag = True
    for s in SET:
        if(T_in[A][1] != '[]' and T_in[B][1] != '[]'):
            if(Find(s, int(T_in[A][1])) != Find(s, int(T_in[B][1]))):
                flag = False
        if(T_in[A][2] != '[]' and T_in[B][2] != '[]'):
            if(Find(s, int(T_in[A][2])) != Find(s, int(T_in[B][2]))):
                flag = False

    return flag


# ## 求异法分割子集

# In[15]:

def Divide(SET):
    SET_new = []
    Finished = False
    #for k in range(len(SET)):
    k = 0
    while(k < len(SET)):
        set_num = len(SET[k])
        if(set_num==1):    # 1个元素保留
            pass
        elif(set_num==2):    # 2个元素
            if(not Equal(SET[k][0], SET[k][1])):
                SET_new.append(SET[k][1])
                SET[k].remove(SET[k][1])
                break
        elif(set_num>=3):    # 3个以上元素
            for j in range(set_num-2):    # 长度为3的窗口向右滑动
                if(Equal(SET[k][j+1], SET[k][j+0])):
                    if(not Equal(SET[k][j+2], SET[k][j+1])):    # 第3个为异
                        SET_new.append(SET[k][j+2])
                        SET[k].remove(SET[k][j+2])
                        k -= 1
                        break
                    else:
                        continue
                else:
                    if(Equal(SET[k][j+2], SET[k][j+1])):    # 第1个为异
                        SET_new.append(SET[k][j+0])
                        SET[k].remove(SET[k][j+0])
                    else:
                        if(Equal(SET[k][j+2], SET[k][j+0])):    # 第2个为异
                            SET_new.append(SET[k][j+1])
                            SET[k].remove(SET[k][j+1])
                        else:
                            SET_new.append(SET[k][j+1])
                            SET[k].remove(SET[k][j+1])
                            SET_new.append(SET[k][j+2])
                            SET[k].remove(SET[k][j+2])
                    k -= 1
                    break
        k += 1

    if(SET_new != []):
        SET.append(SET_new)
    else:
        Finished = True
    
    return SET, Finished


# In[16]:

SET = InitSet(T_in)
print('初始化分割子集:', SET)

while(1):
    print(SET)
    SET, Finished = Divide(SET)
    if(Finished):    # 无新集合(不可再分割)时，结束分割
        break
        
print('最小化分割后集合:', SET)


# ### 查找集合中的索引

# In[17]:

def IndexOfSet(SET, x):
    for i in range(len(SET)):
        if(Find(SET[i], x)):
            return i
    return -1


# ### 生成DFA表

# In[18]:

DFA2 = []
for i in range(len(SET)):
    L = []
    L.append(i)
    
    x = SET[i][0]    # 原始元素
    if(T_in[x][1]=='[]'):
        L.append([])
    else:
        y = int(T_in[x][1])    # 输入为0，跳转到的下一状态
        a = IndexOfSet(SET, y)    # 该状态在新集合中的下标
        L.append(a)
    
    if(T_in[x][2]=='[]'):
        L.append([])
    else:
        z = int(T_in[x][2])    # 输入为1，跳转到的下一状态
        b = IndexOfSet(SET, z)    # 该状态在新集合中的下标
        L.append(b)
    
    if(int(T_in[x][3]) == 1):    # 记录该状态是否为接受(结束)状态
        L.append(1)
    else:
        L.append(0)
    
    DFA2.append(L)
    
DFA2


# In[19]:

print('最小化后DFA表')
print('S\t0\t1\tE')
for i in range(len(DFA2)):
    print('%s\t%s\t%s\t%s' %(i, DFA2[i][1], DFA2[i][2], DFA2[i][3]))


# ### 输出最小化DFA

# In[20]:

path = './Data/'+file_name2+'_min.txt'
fout = open(path, 'w')
for i in DFA2:
    k = '\t'.join([str(j) for j in i])
    fout.write(k+"\n")
fout.close()


# In[21]:

T_out = []
path = './Data/'+file_name2+'_min.txt'
fin = open(path)
lines = fin.readlines()
for line in lines:
    T_out.append([])
    T_out[len(T_out)-1] = line.rstrip().split('\t')

T_out


# ### 测试符号串

# In[22]:

def Test(s, DFA):
    n = len(s)
    flag = False
    
    state = IndexOfSet(SET, int(B))    # 初始化当前状态为开始状态
    print('状态转移序列:', end='  ')
    print(state, end='    ')
    index = 0
    while(index < n):
        x = s[index]
        if(str(x) not in C):
            print('ERROR')
            print('Unsuccessfully !')
            break
        else:
            if(x==C[0]):
                y = DFA[state][1]
                if(y != []):
                    state = y
                else:
                    print('ERROR')
                    print('Fail !')
                    break
            elif(x==C[1]):
                y = DFA[state][2]
                if(y != []):
                    state = y
                else:
                    print('ERROR')
                    print('Fail !')
                    break
            else:
                print('ERROR')
                print('Fail !')
                break
            
            print(state, end='    ')
            if(index == n-1):
                if(DFA[state][3] == 1):
                    print('END')
                    flag = True
                    print('Successfully !')
                    break
                else:
                    print('NOT END')
        
        index += 1
    
    #return flag


# In[24]:

Input_str = input('输入符号串: ')
Test(Input_str, DFA2)


# #### NFA1测试符号串

# In[25]:

String1_1 = '011'
print('输入串:', String1_1)
Test(String1_1, DFA2)

String1_2 = '0101'
print('\n输入串:', String1_2)
Test(String1_2, DFA2)

String1_3 = '1101011'
print('\n输入串:', String1_3)
Test(String1_3, DFA2)

String1_4 = '11100'
print('\n输入串:', String1_4)
Test(String1_4, DFA2)


# #### NFA2测试符号串

# In[26]:

String2_1 = '0011'
print('输入串:', String2_1)
Test(String2_1, DFA2)

String2_2 = '01101011'
print('\n输入串:', String2_2)
Test(String2_2, DFA2)

String2_3 = '1101011'
print('\n输入串:', String2_3)
Test(String2_3, DFA2)

String2_4 = '11100'
print('\n输入串:', String2_4)
Test(String2_4, DFA2)


# #### NFA3测试符号串

# In[27]:

String3_1 = '010'
print('输入串:', String3_1)
Test(String3_1, DFA2)

String3_2 = '010010'
print('\n输入串:', String3_2)
Test(String3_2, DFA2)

String3_3 = '10010100'
print('\n输入串:', String3_3)
Test(String3_3, DFA2)

String3_4 = '1001011'
print('\n输入串:', String3_4)
Test(String3_4, DFA2)

