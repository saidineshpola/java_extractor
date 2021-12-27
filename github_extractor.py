import base64
import json
import requests
import os
import re
import pandas as pd
df=pd.DataFrame()
def get_javafiles_from_user(user:str,repo:str,branch:str)-> list:
    url = "https://api.github.com/repos/{}/{}/git/trees/{}?recursive=1".format(user, repo,branch)
    r = requests.get(url)
    res = r.json()
    #lists= list(res["tree"])
    files_url=[]
    if not "tree" in res:
        if branch !="main":
            return get_javafiles_from_user(user,repo,"main")
        else:
            return []    
    # re_string=(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)
    for file in res["tree"]:
        #print(file["path"].split('.')[-1])
        if file["path"].split('.')[-1]=='java':
            #url_str=os.path.join('https://github.com',user,repo,'blob','master',file["path"])
            files_url.append(file["path"])
            # print(file["path"])
    # print(files[0])
    return files_url

def github_read_file(username, repository_name, file_path, github_token=None):
    headers = {}
    if github_token:
        headers['Authorization'] = f"token {github_token}"
        
    url = f'https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}'
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    file_content = data['content']
    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()

    return file_content

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
    if len(x)==0:
        return []
    for tp in x:
        i=str(tp[0])
        # print(i)
        try:
            sp=txt.split(i)
        except:
            print(i)    
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
def user_repos():
    df_list=[]
    li=[]
    results = requests.get('https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc').json()
    for repo in results['items']:
        li.append(repo['html_url'])
    # base_url="https://github.com/"
    for _,i in enumerate(li):
        #temp=_,i.text.strip(),new_url
        sp=i.split('/')
        username = sp[-2]
        repository_name = sp[-1]
        file_path = get_javafiles_from_user(username,repository_name,'master') #'package.json'
        for path in file_path:
            file_content = github_read_file(username, repository_name,path, github_token=github_token)
            data = file_content
            text_java_list=get_jtext(data)
            try:
                df_list=df_list+text_java_list
            except:
                continue
            #print(data['name'])
    df=pd.DataFrame(df_list,columns=['jtext'])
    df.to_csv('data.csv')
    print(df.head()) 

github_token = ''

if __name__ == '__main__':
    user_repos()
