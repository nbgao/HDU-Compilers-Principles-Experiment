
# coding: utf-8

# In[15]:

import sys
if __name__ == "__main__":
    while True:
        String = input('请输入字符串: ')
        length = len(String)
        String += '$'
        print('%s\n' % String)

        index = 0
        E()
        if String[index] == '$':
            print('\n输入串为合法表达式!\n\n')
        else:
            print('\n输入串为非法表达式!\n\n')

        String = ""
        index = 0


# In[7]:

def E():
    print("E->TE'")
    T()
    E_()


# In[8]:

def E_():
    global index
    if String[index] == '+':
        print("E'->+TE'")
        index += 1
        T()
        E_()
    else:
        print("E'->ε")


# In[9]:

def T():
    print("T->FT'")
    F()
    T_()


# In[10]:

def T_():
    global index
    if String[index] == '*':
        print("T'->*FT'")
        index += 1
        F()
        T_()
    else:
        print("T->ε")


# In[11]:

def F():
    global index
    if String[index] == '(':
        index += 1
        E()
        if String[index] == ')':
            print("F->(E)")
            index += 1
        else:
            print("\n输入串为非法表达式!\n\n")
            sys.exit()
    elif String[index] == 'i':
        print("F->i")
        index += 1
    else:
        print('\n输入串为非法表达式!\n\n')
        sys.exit()


# In[ ]:



