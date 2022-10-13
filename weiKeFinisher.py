from requests import session, request
from time import sleep, time
import json
import random

class Weike():
    def __init__(self, uid, token, school):
        self.school = school
        self.header = {
            "userAgent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47",
            "x-token" : token
        }
        self.uid = uid
        self.ssion = session()

    def get_tasks(self):
        data = {
            "userId":     self.uid,
            "tenantCode": self.school,
            "limit" : 2
        }
        url = "https://weiban.mycourse.cn/pharos/index/listStudyTask.do?timestamp=" + str(int(time()))
        info = self.ssion.post(url, data=data,headers=self.header,verify = False)
        res = json.loads(info.text)['data']
        return res


    def get_category(self, userprojectid):
        url = "https://weiban.mycourse.cn/pharos/usercourse/listCategory.do?timestamp=" + str(int(time()))
        data = {
            "userProjectId": userprojectid,
            "chooseType":    "3",
            "userId":        self.uid,
            "tenantCode":    self.school
        }
        info = info = self.ssion.post(url, data=data,headers=self.header,verify = False)
        res = json.loads(info.text)['data']
        return res
        
    def get_courses(self, userprojectid, categorycode):
        url = "https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp=" + str(int(time()))
        data = {
            "userProjectId": userprojectid,
            "chooseType":    "3",
            "categoryCode":  categorycode,
            "name": "",
            "userId":   self.uid,
            "tenantCode":    self.school
        }
        info = self.ssion.post(url, data=data,headers=self.header,verify = False)
        res = json.loads(info.text)['data']
        return res

    def do_course(self, userprojectid, courseid, userCourseId):
        url1 = "https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp=" + str(int(time()))
        data = {
            "courseId":  courseid,
            "userProjectId": userprojectid,
            "tenantCode":    self.school,
            "userId":   self.uid
        }
        ans1 = self.ssion.post(url1, data=data,headers=self.header, verify = False)
        # print(ans1.text)
        
        url2 = "https://weiban.mycourse.cn/pharos/usercourse/getCourseUrl.do?timestamp=" + str(int(time()))
        ans2 = self.ssion.post(url2, data=data,headers=self.header, verify=False)
        # print(ans2.text)

        sleep(17)

        url3 = "https://weiban.mycourse.cn/pharos/usercourse/finish.do?userCourseId=" +  userCourseId + "&tenantCode="+ self.school
        ans3 = self.ssion.get(url3, headers=self.header, verify=False)
        # print(ans3.text)

    def do_all(self):
        cnt = 0
        tasks = self.get_tasks()
        for task in tasks:
            userProjectId = task['userProjectId']
            categories = self.get_category(userProjectId)
            for category in categories:
                categoryCode = category['categoryCode']
                courses = self.get_courses(userProjectId, categoryCode)
                for course in courses:
                    if course['finished'] == 1:
                        continue
                    courseId = course['resourceId']
                    userCourseId = course['userCourseId']
                    self.do_course(userProjectId, courseId, userCourseId)