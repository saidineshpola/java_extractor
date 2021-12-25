import requests
results = requests.get('https://api.github.com/search/repositories?q=language:java&sort=stars&order=desc').json()

for repo in results['items']:
    print(repo['name'])
    print(repo['html_url'])
    sp=repo['html_url'].split('/')
    print(sp[-1],sp[-2])
    #print(repo.keys())
    break
        




# from github import Github


# ACCESS_TOKEN='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'
# g = Github(ACCESS_TOKEN)
# topic='java'


# repos = g.search_repositories(query=f'topic:{topic} org:{ORGANIZATION}')
# for repo in repos:
#     print(repo)