#include<stdio.h> 
#include<string.h> 
void main() 
{ 
char input[100], l[50],r[50],temp[10],tempprod[20],productions[25][50]; int 
i=0,j=0,flag=0,consumed=0; 
printf(“Enter the Productions:”); 
scanf(“ %ls->%s”, l, r); 
printf(“ %s”, r); 
while(sscanf(r+consumed, “ % [^l] s”, temp) == 1 &&consumed<=strlen(r)) 
{ 
if(temp[0] == l[0]) 
{ 
flag = 1; 
sprintf(productions[i++], “%s->%s%s ‘\0”, l,temp+1,1); 
} 
else 
} 
sprintf(productions[i++], “%s->%s%s ‘\0”,l, temp,1); 
consumed += strlen(temp)+1; 
if(flag==1) 
{ 
sprintf(productions[i++], “%s->€ \0”, 1); 
printf(“the productions after eliminating left recursion are:\n”); 
for(j=0;j<i;j++) 
printf(“%s \n “, productions[j]); 
} 
else 
printf(“ The Given Grammar has no Left Recursion”); 
}
#include<stdio.h> 
#include<conio.h> 
#include<string.h> 
char input[100]; 
int i,l; 
int main() 
{ 
printf("recursive decent parsing for the grammar"); 
printf("\n E->TEP|\nEP->+TEP|@|\nT->FTP|\nTP->*FTP|@|\nF- 
>(E)|ID\n"); 
printf("enter the string to check:"); 
scanf("%s",input); 
if(E()){ 
if(input[i]=='$') 
printf("\n string is accepted\n"); else 
printf("\n string is not accepted\n"); 
} 
} 
E(){ 
if(T()){ 
if(EP()) 
return(1); 
else 
return(0); 
} 
else 
return(0); 
} 
EP(){ 
if(input[i]=='+'){ 
i++; 
if(T()){ 
if(EP()) 
return(1); else return(0); 
} 

else 
return(1); 
} 
} 
T(){ 
if(F()){ 
if(TP()) 
return(1); 
else 
return(0); 
} 
else 
return(0); 
printf("String is not accpeted\n"); 
} 
TP(){ 
if(input[i]=='*'){ 
i++; 
if(F()){ 
if(TP()) 
return(1); 
else 
return(0); 
} 
else 
return(0); 
printf("The string is not accepted\n"); 
} 
else 
return(1); 
} 
F(){ 
if(input[i]=='('){ 
i++; 
if(E()){ 
if(input[i]==')'){ 
i++; 
return(1); 
} 
else 
{ 
return(0); 

printf("String is not accepted\n"); 
} 
} 
else 
return(0); 
} 
else if(input[i]>='a'&&input[i]<='z'||input[i]>='A'&&input[i]<='Z') 
{ 
i++; 
return(1); 
} 
else 
return(0); 
} 
