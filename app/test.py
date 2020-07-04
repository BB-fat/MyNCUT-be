import requests
import json

params = {'avatarUrl': 'avatarUrl', 'nickName': 'nickName'}
url_ip = "http://localhost:8080"
url = url_ip + "/test"


res = requests.get(url)# data=params,headers={"Token":"001tiITq09tJFl10qATq0jb0Uq0tiITD"})
print(res.content)


# params = {'code': 'sssssssss'}
# url_ip = "http://localhost:8001"
# url = url_ip + "/v1/auth"

# res = requests.post(url, data=params)
# print(res.content)    


