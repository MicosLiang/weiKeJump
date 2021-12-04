import requests
import re
import json
import ssl
import time

url = input("enter url: ")
tenantCode = "73000001"
chooseType = "3"
userProjectId = re.findall(r'projectId=(.*?)&',url)[0]

op = {
    "userProjectId": userProjectId,
    "chooseType" : 3,
    "tenantCode" : tenantCode
}
ourl = "https://weiban.mycourse.cn/pharos/usercourse/listCategory.do?timestamp=1638593420"
response = requests.request("post", ourl,params=op)
blocks = json.loads(response.text)["data"]
cnt = 0
for k in blocks:
    categoryCode = k["categoryCode"]
    params = {
        "userProjectId" : userProjectId,
        "categoryCode" : categoryCode,
        "tenantCode" : tenantCode,
        "chooseType" : chooseType
    }
    #print(params)
    aimUrl = "https://weiban.mycourse.cn/pharos/usercourse/listCourse.do"
    response = requests.request("post", aimUrl,params=params)
    ans = json.loads(response.text)
    userCourseIds = []
    for i in ans["data"]:
        userCourseIds.append(i["userCourseId"])
    furl = "https://weiban.mycourse.cn/pharos/usercourse/finish.do"
    for i in userCourseIds:
        fp = {
            "userCourseId": i,
            "tenantCode" : tenantCode
        }
        print(fp)
        # cnt+=1
        fk = requests.request("get", furl, params=fp)
        print(fk.text + i)
        time.sleep(40)
print(cnt)
