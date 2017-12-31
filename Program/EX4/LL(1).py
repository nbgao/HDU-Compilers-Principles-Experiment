
# coding: utf-8

# ## 输入字符串

# In[31]:

String = [[] for row in range(6)]
String[0] = ['i+i*i', '(i+i)*i+i', '(i+i)*i', 'i-i', 'i**i+i']
String[1] = ['a', 'ddb', 'efao', 'ba', 'o']
String[2] = ['a', '(a)', '(a,a)', 'a,a', '(a)a']
String[3] = ['a', 'aade', 'aadbbe', 'ab', '']
String[4] = ['i', 'ii+', 'ii-', 'i/i', '(i+i)']
String[5] = ['ix', 'ix,x', 'fx', 'i', 'f']


# ## 主程序

# In[34]:

if __name__ == "__main__":
    import pprint
    
    Grammers = [[] for g in range(6)]
    Grammers[0] = ['E::E+T|T', 'T::T*F|F', 'F::(E)|i']
    Grammers[1] = ['S::MH|a', 'H::LSo|ε', 'K::dML|ε', 'L::eHf', 'M::K|bLM']
    Grammers[2] = ['S::a|ε|(T)', 'T::T,S|S']
    Grammers[3] = ['A::aABe|a', 'B::Bb|d'] ## 需要提取左公因子
    Grammers[4] = ['E::ET+|ET-|T', 'T::TF*|TF/|F', 'F::(E)|i'] ## 消除左递归+ 提取左公因子
    Grammers[5] = ['A::BC', 'B::i|f', 'C::x,C|x']
    
    grammer_num = int(input('请输入选择的文法规则序号: '))
    
    Grammer = Grammers[grammer_num]
    print('\n文法规则')
    print(Grammer)
    
    Grammer_new = EliminateLeftRecursion(Grammer)
    print('\n消除左递归后文法')
    print(Grammer_new)
    
    Grammer_new = ExtractLeftCommonFactor(Grammer_new)
    print('\n提取左公因子后文法')
    print(Grammer_new)
    
    start = Grammer[0][0]
    print('\n开始符号:', start)
    
    VN = getVN(Grammer_new)
    print('\n非终结符')
    print(VN)
    
    VT = getVT(Grammer_new)
    print('\n终结符')
    print(VT)
    
    FIRST = getFIRST(Grammer_new)
    print('\nFIRST集')
    pprint.pprint(FIRST)
    
    FOLLOW = getFOLLOW(Grammer_new)
    print('\nFOLLOW集')
    pprint.pprint(FOLLOW)
    
    SELECT = getSELECT(Grammer_new)
    print('\nSELECT集')
    pprint.pprint(SELECT)
    
    print('\n判断是否为LL(1)文法:')
    LL1_Judge(Grammer_new)
    
    PredictAnalyzeTable = AnalyzeTable(Grammer_new, FIRST, FOLLOW)
    print('\nLL(1)预测分析表')
    PrintAnalyzeTable(PredictAnalyzeTable)
    
    print('\n字符串分析判断')
    for string in String[grammer_num]:
         AnalyzeJudge(start, string)
    


# ## 消除左递归

# In[35]:

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
                result2.append('ε')
                rightExpression2 = '|'.join(result2)
                expression2 = leftSymbolNew + rule[1:rightIndex] + rightExpression2


                Grammer_new += [expression1]
                Grammer_new += [expression2]
        else:
            Grammer_new += [rule]
    
    return Grammer_new


# In[36]:

Grammer_new = EliminateLeftRecursion(Grammer)
Grammer_new


# ### 求最长公共前缀

# In[37]:

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

# In[38]:

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
                        postfix.append('ε')
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


# In[39]:

Grammer_new = ExtractLeftCommonFactor(Grammer_new)
Grammer_new


# ## 获取非终结符

# In[40]:

def getVN(Grammer):
    VN = []
    for g in Grammer:
        t = g.find('::')
        ch = g[:t]
        if ch not in VN:
            VN.append(ch)
    return VN


# In[41]:

VN = getVN(Grammer_new)
print(VN)


# ## 获取终结符

# In[42]:

def getVT(Grammer):
    VT = []
    VN = getVN(Grammer)
    VN.append("::")
    VN.append("'")
    VN.append("|")
    for g in Grammer:
        for s in VN:
            g = g.replace(s, "")
        for ch in g:
            if ch not in VT:
                VT.append(ch)
    
    return VT


# In[43]:

VT = getVT(Grammer_new)
print(VT)


# ### 分割表达式

# In[44]:

def Split(Expression):
    List_char = []
    n = len(Expression)
    k = 0
    for i in range(n):
        ch = Expression[i]
        if ch == "'":
            List_char[k-1] += ch
        else:
            List_char.append(ch)
            k += 1
    return List_char


# ### 获取子表达式

# In[45]:

def SubExpression(Grammer):
    _Grammer = {}
    for grammer in Grammer:
        grammer_split = grammer.split('::')
        _Grammer[grammer_split[0]] = grammer_split[1]
        
    subExpressions = {}
    for vn, rightExp in _Grammer.items():
        subExpressions[vn] = [subExp for subExp in rightExp.split('|')]
        
    #print(subExpressions)
    return subExpressions


# In[46]:

SubExpression(Grammer_new)


# ### 获取文法子规则

# In[47]:

def SubRules(Grammer):
    subRules = []
    for g in Grammer_new:
        leftExp = g.split('::')[0]
        rightExps = g.split('::')[1]
        subRules += [leftExp + "::" + rightExp for rightExp in rightExps.split('|')]
    return subRules


# In[48]:

SubRules(Grammer_new)


# ## 计算FIRST集

# In[49]:

def getFIRST(Grammer_new):
    First = SubExpression(Grammer_new)
    
    FIRST = {}
    for vn in VN:
        FIRST[vn] = []
    
    lock = 1
    while First and lock<100:
        for vn in VN:
            # if First.has_key(vn):
            if vn in First.keys():
                first = First[vn]
                for chs in first:
                    ch = chs[0]
                    if ch in VT:  # 子规则第一个符号是终结符
                        FIRST[vn].append(ch)
                        First[vn].remove(chs)
                    else:
                        if ch not in First:  # ch是非终结符
                            FIRST[vn] += FIRST[ch]                            
                            First[vn].remove(chs)
                            if 'ε' in FIRST[ch]:  # 终结符中有'ε'，那么下一个符号的First集也需要被继续计算
                                FIRST[vn].remove('ε')
                                if len(chs) == 1:   # 若为最后一个符号，则加入#
                                    First[vn].append('ε')
                                else:    # 若不是最后一个符号，增加后续字符
                                    First[vn].append(chs[1:])   
                        else:
                            pass
                if not First[vn]:
                    First.pop(vn)
        lock += 1
    
    return FIRST


# In[50]:

FIRST = getFIRST(Grammer_new)
FIRST


# ## 计算FOLLOW集

# In[51]:

def getFOLLOW(Grammer):
    Follow = SubExpression(Grammer)
    
    FOLLOW = {}
    for vn in VN:
        FOLLOW[vn] = []
        
    # Rule1 加入文法的开始符号的Follow集
    FOLLOW[VN[0]].append('$')
    
    # Rule2
    FIRST
    FollowLink = {}
    for vn in VN:
        FollowLink[vn] = []
    for vn, expression in Follow.items():
        for subExp in expression:
            subExp = Split(subExp)
            for ch in subExp[:-1]:
                if ch in VN:
                    index = subExp.index(ch) + 1
                    string = subExp[index:]
                    FollowLink[ch].append(''.join(string))
                    
    # print(FollowLink)
    
    for vn, stringList in FollowLink.items():
        for string in stringList:
            string = Split(string)
            for ch in string:
                # print('string',string)
                if ch in VT:
                    FOLLOW[vn].append(ch)
                    break
                else:
                    FirstSetOfChar = FIRST[ch]
                    if 'ε' in FirstSetOfChar:
                        FirstSetOfChar.remove('ε')
                        FOLLOW[vn] += FirstSetOfChar
                    else:
                        FOLLOW[vn] += FirstSetOfChar
                        break
                    
                        
    # Rule3
    # 先求出能推导出 '#' 的非终结符
    NullChar = []
    for vn, subExp in Follow.items():
        if 'ε' in subExp:
            NullChar.append(vn)
    NullChar.append('')
    
    FollowLink2 = {}
    for vn in VN:
        FollowLink2[vn] = []
        
    for vn, subExps in Follow.items():
        for expression in subExps:
            expression = Split(expression)
            index = len(expression) - 1
            while index >= 0:
                ch = expression[index]
                if ch == vn:
                    break
                elif ch in VT:
                    break
                elif ch not in NullChar:
                    FollowLink2[ch].append(vn)
                    break
                else:
                    FollowLink2[ch].append(vn)
                    index -= 1
    # print('FollowLink2', FollowLink2)
    hasFollowChar = []
    notFollowChar = []
    for vn, links in FollowLink2.items():
        if not links:
            hasFollowChar.append(vn)
        else:
            notFollowChar.append(vn)
    # print('hasFollowChar', hasFollowChar)
    # print('notFollowChar', notFollowChar)
    
    lock = 1
    while notFollowChar and lock < 100:
        delChar = []
        for vn in notFollowChar:
            ### if set(FollowLink2[vn]).issubset(set(hasFollowChar)):
            for link in FollowLink2[vn]:
                FOLLOW[vn] += FOLLOW[link]
            delChar.append(vn)
        # print('delChar', delChar)
        # print('hasFollowChar', hasFollowChar)
        # print('notFollowChar', notFollowChar)
        for ch in delChar:
            hasFollowChar.append(ch)
            notFollowChar.remove(ch)
        lock += 1

    for vn in VN:
        FOLLOW[vn] = list(set(FOLLOW[vn]))
    
    return FOLLOW


# In[52]:

FOLLOW = getFOLLOW(Grammer_new)
FOLLOW


# ### 计算SELECT集

# In[53]:

def getSELECT(Grammer):
    subRules = SubRules(Grammer)

    SELECT = {}
    for rule in subRules:
        leftExp, rightExp = rule.split('::')
        #print(leftExp, rightExp)
        if '#' not in rightExp:
            if rightExp[0] in VT:
                SELECT[rule] = rightExp[0]
            elif rightExp[0] in VN:
                SELECT[rule] = FIRST[rightExp[0]]
        else:
            SELECT[rule] = FOLLOW[leftExp]
    
    return SELECT


# In[54]:

SELECT = getSELECT(Grammer_new)
SELECT


# ## LL(1)文法判断

# In[55]:

def LL1_Judge(Grammer):
    isLL1 = True
    Select = SubExpression(Grammer)

    for vn, subExps in Select.items():
        sub_num = len(subExps)
        if sub_num > 1:
            for i in range(sub_num-1):
                for j in range(i+1, sub_num):
                    rule1 = vn + '::' + subExps[i]
                    rule2 = vn + '::' + subExps[j]
                    select1, select2 = SELECT[rule1], SELECT[rule2]
                    intersection = list(set(select1).intersection(set(select2)))
                    if intersection != []:    # 交集不为空
                        isLL1 = False
                        break

    if isLL1 == True:
        print('是LL(1)文法')
    else:
        print('不是LL(1)文法')


# In[56]:

LL1_Judge(Grammer_new)


# ### 表达式分析

# In[57]:

def ExpressionAnalyze(expression, FITST, FOLLOW):
    VT
    VN
    leftExp, rightExp = expression.split('::')
    meetChars = []
    for ch in rightExp:
        if ch == 'ε':
            meetChars += FOLLOW[leftExp]
            break
        elif ch in VT:
            meetChars.append(ch)
            break
        else:
            meetChars += FIRST[ch]
            if 'ε' not in FIRST[ch]:
                break
            else:
                meetChars.remove('ε')
    
    return leftExp, meetChars


# ## 预测分析表

# In[58]:

def AnalyzeTable(Grammer, FIRST, FOLLOW):
    VT.remove('ε')
    VT.append('$')
    Table = {}
    
    for vn in VN:
        Table[vn] = {}
        for vt in VT:
            Table[vn][vt] = 'ERROR'
    
    subRules = []
    for g in Grammer:
        leftExp = g.split('::')[0]
        rightExps = g.split('::')[1]
        subRules += [leftExp + "::" + rightExp for rightExp in rightExps.split('|')]
    
    for rule in subRules:
        leftExp, meetChars = ExpressionAnalyze(rule, FIRST, FOLLOW)
        for ch in meetChars:
            Table[leftExp][ch] = rule
        
    return Table


# In[59]:

AT = AnalyzeTable(Grammer_new, FIRST, FOLLOW)
AT


# ### 打印分析表

# In[60]:

def PrintAnalyzeTable(Table):
    print('\t\t', end='');
    for vt in VT:
        if vt=='ε':
            print('$', end='\t\t')
        else:
            print(vt, end='\t\t')
    print()

    for vn in VN:
        print(vn, end='\t\t')

        for vt in VT:
            if(Table[vn][vt] == 'ERROR'):
                print('\t', end='\t')
            else:
                if(len(Table[vn][vt]) < 8):
                    print(Table[vn][vt], end='\t\t')
                else:
                    print(Table[vn][vt], end='\t')
        print()
    print()


# In[61]:

PrintAnalyzeTable(AT)


# ## 字符串分析判断

# In[62]:

def AnalyzeJudge(start, String):
    isMatch = False
    Stack = ['$', start]
    Input = list(String) + ['$']
    print('判断字符串', String)
    print('%-28s%-14s%s' %('栈', '输入串', '输出产生式'))
    
    try:
        while Stack:
            x = Stack[-1]
            y = Input[0]
            print("%-18s%18s%10s" % ("".join(Stack), "".join(Input), ""), end='')
            if x == y:  # 相同则同时弹出
                if x != '$':
                    Stack.pop()
                    Input.pop(0)
                else:  # 到达栈底
                    Stack.pop()
                    isMatch = True
                print()
            elif x in VN:
                Stack.pop()
                '''
                if y=='$':
                    y = 'ε'
                '''
                expression = PredictAnalyzeTable[x][y]
                if expression == "ERROR":
                    print('ERROR')
                    raise ValueError
                print(expression)
                t = expression.find('::')+2
                if Split(expression[t:])[::-1] != ['ε']:
                    Stack += Split(expression[t:])[::-1]  # 逆序加入栈
            elif x == '$':  # 若栈先空，则出错
                print('ERROR')
                break
    except Exception as e:
        print('ERROR')
        pass

    if isMatch:
        print('输入串%s符合文法\n' % String)
    else:
        print('输入串%s不符合文法\n' % String)
    
    return isMatch


# In[ ]:



