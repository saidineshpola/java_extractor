import requests
import re
user = "saidineshpola"
repo = "finetuning-hf-gpt6b"

url = "https://api.github.com/repos/{}/{}/git/trees/main?recursive=1".format(user, repo)
# url = "https://api.github.com/repos/{}/{}/master?recursive=1".format(user, repo)
r = requests.get(url)
res = r.json()
print(res["tree"])
# list=list(res["tree"])
# files=[]
# # re_string=(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)
# for file in res["tree"]:
#     #print(file["path"].split('.')[-1])
#     if file["path"].split('.')[-1]=='sh':
#         files.append(file["path"])
#         # print(file["path"])
# print(files[0])
