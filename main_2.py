import re
import os
import requests
import pdb
from bs4 import BeautifulSoup
import pandas as pd
# github_token="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"
df=pd.DataFrame()
df_list=[]
# url="https://github.com/search?o=desc&p=?&q=java+repositories&s=stars&type=Repositories"

def get_javafiles_from_user(user:str,repo:str)-> list:
    url = "https://api.github.com/repos/{}/{}/git/trees/master?recursive=1".format(user, repo)
    r = requests.get(url)
    res = r.json()
     #lists= list(res["tree"])
    files_url=[]
    if not "tree" in res:
        return []
    # re_string=(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)
    for file in res["tree"]:
        #print(file["path"].split('.')[-1])
        if file["path"].split('.')[-1]=='java':
            url_str=os.path.join('https://github.com',user,repo,file["path"])
            files_url.append(url_str)
            # print(file["path"])
    # print(files[0])
    return files_url

def extract_codes_from_url(jfile:str)->str:
    # page=requests.get('https://github.com/LibrePDF/OpenPDF/blob/master/openpdf/src/main/java/com/lowagie/text/alignment/HorizontalAlignment.java')
    print(jfile)
    page=requests.get(jfile)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    print(soup.prettify())
    pdb.set_trace()
    code = soup.find('table',class_='highlight tab-size js-file-line-container js-code-nav-container js-tagsearch-file').find_all('tr',recursive=False)
    text=""
    for i,row in enumerate(code):
        text=text+(str(row.text))
        #text=row.find('tr').get_text()
        #print(str(i)+str(row.text))   
        #   
    return text

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

def get_jtext(txt:str):
    # with open('text.txt','r') as t:
    #     txt=t.read()
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
        return jtext
    # print(len(jtext))


if __name__=='__main__':
    for x in range(1):
        # url=f"https://github.com/search?o=desc&p={x}&q=java+repositories&s=stars&type=Repositories"
        # page=requests.get(url)
        # # with open('sample.html','r') as f:
        # #     soup=BeautifulSoup(f,'html.parser')
        # # print(soup.prettify) 
        # soup=BeautifulSoup(page.text,'html.parser')
        # # trail=soup.find('div').get_text()
        # # print(soup)
        # li=soup.find_all('div',class_='f4 text-normal')
        # urls=[]
        # Repo=[]
        li=[]
        results = requests.get('https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc').json()
        for repo in results['items']:
            li.append(repo['html_url'])
        base_url="https://github.com/"
        for _,i in enumerate(li):
            #temp=_,i.text.strip(),new_url
            sp=i.split('/')
            java_files_url=get_javafiles_from_user(sp[-2],sp[-1])
            for file_url in java_files_url:
                code=extract_codes_from_url(file_url)
                text_java_list=get_jtext(code)
                df_list=df_list+text_java_list
            #Repo.append(i.text.strip())
            #urls.append(new_url)
            #print(i.text.strip(),new_url)
        #  df_list=list(zip(Repo,urls))
    df=pd.DataFrame(df_list,columns=['jtext'])
    df.to_csv('data.csv')
    print(df.head()) 