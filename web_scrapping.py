from bs4 import BeautifulSoup
import requests
import pandas as pd
from github import Github
df=pd.DataFrame()

ACCESS_TOKEN='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'
g = Github(ACCESS_TOKEN)
repos = g.search_repositories(query=f'topic:{topic} org:{ORGANIZATION}')
for repo in repos:
    print(repo)

url="https://github.com/search?o=desc&p=2&q=java+repositories&s=stars&type=Repositories"
for x in range(1,2):
    url=f"https://github.com/search?o=desc&p={x}&q=java+repositories&s=stars&type=Repositories"
    page=requests.get(url)
    # with open('sample.html','r') as f:
    #     soup=BeautifulSoup(f,'html.parser')
    #print(soup.prettify) 
    soup=BeautifulSoup(page.text,'html.parser')
    # trail=soup.find('div').get_text()
    # print(trail)
    print(soup.prettify())
    li=soup.find_all('div',class_='f4 text-normal')
    print(li)
    urls=[]
    Repo=[]
    df_list=[]
    base_url="https://github.com/"
    for _,i in enumerate(li):
        for a in i.findAll('a'):
            new_url=base_url+a["href"]
            #temp=_,i.text.strip(),new_url

        Repo.append(i.text.strip())
        urls.append(new_url)
        #print(i.text.strip(),new_url)
    df_list=list(zip(Repo,urls))
    df=pd.DataFrame(df_list,columns=['Repository','URL'])
print(df.head())    


    
