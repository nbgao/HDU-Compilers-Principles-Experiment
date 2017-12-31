#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cctype>
#include <string>
#include <cstring>

using namespace std;

void AnalyzeId(FILE *fout, char *s)
{
    if(isalpha(s[0]))
    {
        if(strcmp(s, "int")==0)
        {
            printf("(5, kw_int)\n");
            fprintf(fout, "(5, kw_int )\n");
        }else if(strcmp(s, "char")==0){
            printf("(6, kw_char)\n");
            fprintf(fout, "(6, kw_char)\n");
        }else if(strcmp(s, "void")==0){
            printf("(7, kw_void)\n");
            fprintf(fout, "(7, kw_void)\n");
        }else if(strcmp(s, "if")==0){
            printf("(8, kw_if)\n");
            fprintf(fout, "(8, kw_if)\n");
        }else if(strcmp(s, "else")==0){
            printf("(9, kw_else)\n");
            fprintf(fout, "(9, kw_else)\n");
        }else if(strcmp(s, "switch")==0){
            printf("(10, kw_switch)\n");
            fprintf(fout, "(10, kw_switch)\n");
        }else if(strcmp(s, "case")==0){
            printf("(11, kw_case)\n");
            fprintf(fout, "(11, kw_case)\n");
        }else if(strcmp(s, "default")==0){
            printf("(12, kw_default)\n");
            fprintf(fout, "(12, kw_default)\n");
        }else if(strcmp(s, "while")==0){
            printf("(13, kw_while)\n");
            fprintf(fout, "(13, kw_while)\n");
        }else if(strcmp(s, "do")==0){
            printf("(14, kw_do)\n");
            fprintf(fout, "(14, kw_do)\n");
        }else if(strcmp(s, "for")==0){
            printf("(15, kw_for)\n");
            fprintf(fout, "(15, kw_for)\n");
        }else if(strcmp(s, "break")==0){
            printf("(16, kw_break)\n");
            fprintf(fout, "(16, kw_break)\n");
        }else if(strcmp(s, "continue")==0){
            printf("(17, kw_continue)\n");
            fprintf(fout, "(17, kw_continue)\n");
        }else if(strcmp(s, "return")==0){
            printf("(18, kw_return)\n");
            fprintf(fout, "(18, kw_return)\n");
        }else{
            printf("(1, id: %s)\n", s);
            fprintf(fout, "(1, id: %s)\n", s);
        }
    }else{
        int len = strlen(s);
        int count = 0;

        for(int i=0;i<len;i++)
            if(isdigit(s[i]))
                count++;

        if(s[0]=='_' && isalnum(s[1]))
        {
            printf("(1, id: %s)\n", s);
            fprintf(fout, "(1, id: %s)\n", s);
        }else{
            printf("[Undefine]: %s\n", s);
            fprintf(fout, "[Undefine]: %s\n", s);
        }
    }

}


void AnalyzeSymbol(FILE *fout, char *s)
{
    if(strcmp(s, " ")==0)
    {

    }else if(strcmp(s, "\n")==0){

    }else if(strcmp(s, "\t")==0){

    }else if(strcmp(s, "+")==0){
        printf("(19, add)\n");
        fprintf(fout, "(19, add)\n");
    }else if(strcmp(s, "-")==0){
        printf("(20, sub)\n");
        fprintf(fout, "(20, sub)\n");
    }else if(strcmp(s, "*")==0){
        printf("(21, mul)\n");
        fprintf(fout, "(21, mul)\n");
    }else if(strcmp(s, "/")==0){
        printf("(22, div)\n");
        fprintf(fout, "(22, div)\n");
    }else if(strcmp(s, "%")==0){
        printf("(23, mod)\n");
        fprintf(fout, "(23, mod)\n");
    }else if(strcmp(s, "++")==0){
        printf("(24, inc)\n");
        fprintf(fout, "(24, inc)\n");
    }else if(strcmp(s, "--")==0){
        printf("(25, dec)\n");
        fprintf(fout, "(25, dec)\n");
    }else if(strcmp(s, "!")==0){
        printf("(26, not)\n");
        fprintf(fout, "(26, not)\n");
    }else if(strcmp(s, "&&")==0){
        printf("(27, and)\n");
        fprintf(fout, "(27, and)\n");
    }else if(strcmp(s, "||")==0){
        printf("(28, or)\n");
        fprintf(fout, "(28, or)\n");
    }else if(strcmp(s, "=")==0){
        printf("(29, assign)\n");
        fprintf(fout, "(29, assign)\n");
    }else if(strcmp(s, ">")==0){
        printf("(30, gt)\n");
        fprintf(fout, "(30, gt)\n");
    }else if(strcmp(s, ">=")==0){
        printf("(31, ge)\n");
        fprintf(fout, "(31, ge)\n");
    }else if(strcmp(s, "<")==0){
        printf("(32, lt)\n");
        fprintf(fout, "(32, lt)\n");
    }else if(strcmp(s, "<=")==0){
        printf("(33, le)\n");
        fprintf(fout, "(33, le)\n");
    }else if(strcmp(s, "==")==0){
        printf("(34, equ)\n");
        fprintf(fout, "(34, equ)\n");
    }else if(strcmp(s, "!=")==0){
        printf("(35, nequ)\n");
        fprintf(fout, "(35, nequ)\n");
    }else if(strcmp(s, ",")==0){
        printf("(36, comma)\n");
        fprintf(fout, "(36, comma)\n");
    }else if(strcmp(s, ":")==0){
        printf("(37, colon)\n");
        fprintf(fout, "(37, colon)\n");
    }else if(strcmp(s, ";")==0){
        printf("(38, simcon)\n");
        fprintf(fout, "(38, simcon)\n");
    }else if(strcmp(s, "(")==0){
        printf("(39, lparen)\n");
        fprintf(fout, "(39, lparen)\n");
    }else if(strcmp(s, ")")==0){
        printf("(40, rparen)\n");
        fprintf(fout, "(40, rparen)\n");
    }else if(strcmp(s, "{")==0){
        printf("(41, lbrac)\n");
        fprintf(fout, "(41, lbrac)\n");
    }else if(strcmp(s, "}")==0){
        printf("(42, rbrac)\n");
        fprintf(fout, "(42, rbrac)\n");
    }else{
        printf("[Undefine]: %s\n", s);
        fprintf(fout, "[Undefine]: %s\n", s);
    }

}


void AnalyzeNum(FILE *fout, char *s)
{
    bool flag = true;
    int len = strlen(s);

    if(s[0] == '0')
    {
        if(len>=2 && (s[1]=='x' || s[1]=='X'))      //十六进制
        {
            for(int i=2;i<len;i++)
            if(!((s[i]>='0'&&s[i]<='9') || (s[i]>='a'&&s[i]<='f') || (s[i]>='A'&&s[i]<='F')))
            {
                flag = false;
                break;
            }
        }else{
            for(int i=1;i<len;i++)              //八进制
                if(!(s[i]>='0' && s[i]<='7'))
                {
                    flag = false;
                    break;
                }
        }
    }else{
        for(int i=0;i<len;i++)
            if(!isdigit(s[i]))
            {
                flag = false;
                break;
            }
    }

    if(flag)
    {
        printf("(2, num: %s)\n", s);         //常数变量
        fprintf(fout, "(2, num: %s)\n", s);
    }else{
        printf("[Undefine]: %s\n", s);
        fprintf(fout, "[Undefine]: %s\n", s);
    }
}


void AnalyzeCh(FILE *fout, char *s)
{
    printf("(3, ch: %s)\n", s);
    fprintf(fout, "(3, ch: %s)\n", s);
}


void AnalyzeStr(FILE *fout, char *s)
{
    printf("(4, str: %s)\n", s);
    fprintf(fout, "(4, str: %s)\n", s);
}


int main()
{
    FILE *fin, *fout;
    char file_in[] = "test_input1.txt";
    char file_out[] = "test_output1.txt";
    char ch, s[10000], s_id[110], s_symbol[3], s_num[110], s_ch[4], s_str[110];


    if((fin = fopen(file_in, "r")) == NULL)
    {
        printf("Fail to open the test input file !");
        exit(0);
    }else{
        printf("Open the input file successfully !\n");
    }

    if((fout = fopen(file_out, "w")) == NULL)
    {
        printf("Fail to open the test output file !");
        exit(0);
    }else{
        printf("Open the output file successfully !\n");
    }

    printf("\n----------Start----------\n");
    fprintf(fout, "----------Start----------\n");


    int i = 0, x = 0;

    ch = fgetc(fin);
    while(ch != EOF)
    {
        s[i] = ch;
        s[i+1] = '\0';
        i++;
        ch = fgetc(fin);
    }

    i = 0;
    while(s[i]!='#' && s[i+1]!='#')
    {
        if(isalnum(s[i]) || s[i]=='_')
        {
            s_id[x] = s[i];
            s_id[x+1] = '\0';
            x++;
            i++;

        }else{
            x = 0;
            if((isalpha(s_id[0]) || s_id[0]=='_') && strlen(s_id)!=0 )
                AnalyzeId(fout, s_id);         //识别标识符
            else if(isdigit(s_id[0])){
                int j = 0;
                s_num[j] = s_id[0];
                for(j=1;j<strlen(s_id);j++)
                    s_num[j] = s_id[j];
                s_num[j] = '\0';
                AnalyzeNum(fout, s_num);
            }

            s_id[x] = '\0';

            if(!isalnum(s[i]))
            {
                if((s[i]=='+' && s[i+1]=='+') ||            //双符号
                         (s[i]=='-' && s[i+1]=='-') ||
                         (s[i]=='&' && s[i+1]=='&') ||
                         (s[i]=='|' && s[i+1]=='|') ||
                         (s[i]=='!' && s[i+1]=='=') ||
                         (s[i]=='=' && s[i+1]=='=') ||
                         (s[i]=='<' && s[i+1]=='=') ||
                         (s[i]=='>' && s[i+1]=='=')){
                    s_symbol[0] = s[i];
                    s_symbol[1] = s[i+1];
                    s_symbol[2] = '\0';
                    AnalyzeSymbol(fout, s_symbol);
                    i+=2;
                }else if(s[i]=='\'' && s[i+2]=='\''){       //字符常量
                    s_ch[0] = s[i];
                    s_ch[1] = s[i+1];
                    s_ch[2] = s[i+2];
                    s_ch[3] = '\0';
                    AnalyzeCh(fout, s_ch);
                    i+=3;
                }else if(s[i]=='\"'){           //字符串常量
                    int j = 0;
                    s_str[j] = s[i];
                    for(j=1;s[i+j]!='\"';j++)
                        s_str[j] = s[i+j];
                    s_str[j] = '\"';
                    s_str[j+1] = '\0';
                    AnalyzeStr(fout, s_str);
                    i += j+1;
                }else{
                    s_symbol[0] = s[i];
                    s_symbol[1] = '\0';
                    AnalyzeSymbol(fout, s_symbol);
                    i++;
                }
            }
        }
    }


    printf("----------Finish----------\n");
    fprintf(fout, "----------Finish----------\n");
    printf("\nLexical Analyze was completed.\nThe result has been saved into output file.\n");

    fclose(fin);
    fclose(fout);

    return 0;
}
