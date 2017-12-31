
# coding: utf-8

# In[17]:

Grammers = [[] for i in range(5)]
Grammers[0] = ['E::E+T|T', 'T::T*F|F', 'F::(E)|i']    # 需要消除左递归
Grammers[1] = ['A::aABe|a', 'B::Bb|d']    # 需要消除左递归和提取左公因子
Grammers[2] = ['E::ET+|ET-|T', 'T::TF*|TF/|F', 'F::(E)|i']    # 需要消除左递归和提取左公因子
Grammers[3] = ['E::T+|T-|(E)|+E|-E|i', 'T::ia|ib|ic|a|b|#']    # 需要提取左公因子
Grammers[4] = ['S::a|#|(T)', 'T::T,S|S']    # 需要消除左递归


grammer_num = int(input('请输入选择的文法规则序号: '))

Grammer = Grammers[grammer_num]
print('\n文法规则')
print(Grammer)

Grammer_1 = EliminateLeftRecursion(Grammer)
print('\n消除左递归后文法')
print(Grammer_1)

Grammer_2 = ExtractLeftCommonFactor(Grammer_1)
print('\n提取左公因子后文法')
print(Grammer_2)


# ## 消除左递归

# In[18]:

def EliminateLeftRecursion(Grammer):
    Grammer_new = []
    for rule in Grammer:
        t = rule.find('::')
        rightIndex = t+2
        leftSymbol = rule[:t]
        rightSymbol = rule[rightIndex:]

        rightFirstSymbol = rule[rightIndex]
        #print(leftSymbol, rightSymbol)
        if leftSymbol == rightFirstSymbol:  # 左表达式与右表达式第一个字符相同
                result1 = [symbol for symbol in rule[rightIndex:].split('|') if leftSymbol not in symbol]
                result2 = [symbol for symbol in rule[rightIndex:].split('|') if leftSymbol in symbol]
                
                leftSymbolNew = leftSymbol + "'"
                result1 = [symbol + leftSymbolNew for symbol in result1]
                rightExpression1 = '|'.join(result1)
                expression1 = rule[0:rightIndex] + rightExpression1

                result2 = [symbol.replace(leftSymbol, "") + leftSymbolNew for symbol in result2]           
                result2.append('#')
                rightExpression2 = '|'.join(result2)
                expression2 = leftSymbolNew + rule[1:rightIndex] + rightExpression2


                Grammer_new += [expression1]
                Grammer_new += [expression2]
        else:
            Grammer_new += [rule]
    
    return Grammer_new


# In[19]:

Grammer_new1 = EliminateLeftRecursion(Grammer)
Grammer_new1


# ### 求最长公共前缀

# In[20]:

def LongestCommonPrefix(s1, s2):
    prefix = ''
    l1, l2 = len(s1), len(s2)
    for i in range(min(l1,l2)):
        if s1[i]==s2[i]:
            prefix += s1[i];
        else:
            break
    return prefix


# ## 提取左公因子

# In[21]:

def ExtractLeftCommonFactor(Grammer):
    Grammer_new = []
    for rule in Grammer:
        t = rule.find('::')
        rightIndex = t+2
        leftSymbol = rule[:t]
        rightSymbol = rule[rightIndex:]
        rightExp = [symbol for symbol in rule[rightIndex:].split('|')]
        prefix = ''
        for i in range(len(rightExp)-1):
            for j in range(i+1,len(rightExp)):
                Exp1, Exp2 = rightExp[i], rightExp[j]
                prefix = LongestCommonPrefix(Exp1, Exp2)
                if prefix != '':  # 最长公共前缀非空
                    break
            if prefix != '':
                break

        postfix = []
        if prefix != '':
            index = len(prefix)
            tail = []
            #print('rightExp', rightExp)
            for exp in rightExp:
                if prefix == exp[:index]:  # 表达式中存在前缀
                    if exp[index:] == '':  # 前缀后面无字符
                        postfix.append('#')
                    else:
                        postfix.append(exp[index:])
                else:
                    tail.append(exp)
            #print('postfix', postfix)
            #print('tail', tail)
            # 产生提取左公因子的第1条新语法规则
            leftSymbolNew = leftSymbol + "'"
            rightExp_new1 = prefix + leftSymbolNew
            if tail != []:  # 若尾部表达式不为空，则在新表达式后加上尾部表达式
                rightExp_new2 = ('|').join(tail)
                rightExp_new2 = '|' + rightExp_new2
            else:
                rightExp_new2 = ''
            expression1 = leftSymbol +'::'+ rightExp_new1 + rightExp_new2
            Grammer_new += [expression1]
            #print('expression1', expression1)

            # 产生提取左公因子的第2条新语法规则
            postfix_new = [leftSymbolNew + symbol for symbol in postfix]
            rightExp_new = '|'.join(postfix)
            rightExp_new
            expression2 = leftSymbolNew + '::' + rightExp_new
            Grammer_new += [expression2]
            #print('expression2', expression2)
        else:
            Grammer_new += [rule]
    return Grammer_new


# In[22]:

Grammer_new2 = ExtractLeftCommonFactor(Grammer_new1)
Grammer_new2


# In[ ]:



