import re
# Function to get balanced function after the comment string
def get_data(s:str)-> str:
    count=-9999999
    flag=1
    for _,i in enumerate(s):
        if i=='{' and flag:
            count=1
            flag=0
        elif i=='{' and not flag:
            count=count+1    
        elif i=='}':
            count=count-1
        if count==0:
            return s[0:_+1]       
    if count==0:
        return s
    return ""

if __name__=='__main__':
    with open('text.txt','r') as t:
        txt=t.read()
    # finding comments
    x = re.findall("(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)", txt)
    jtext=[]
    for tp in x:
        i=str(tp[0])
        # print(i)
        sp=txt.split(i)
        if len(sp)>1 :
            fc_text=sp[1]
        else:
            continue
        # print(fc_text)
        fc_text=get_data(fc_text)
        if fc_text=="":
            continue
        jtext.append(i+fc_text)
    print(len(jtext))




# finding function line after comments
# \*\/[\r\n]+([^\r\n]+)


