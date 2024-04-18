import imp
from wsgiref import headers
from requests import session, request
from time import sleep
import json
import random

class weike():
    def __init__(self, sid):
        self.sid = sid
        self.header = {
            "userAgent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47",
            "x-token" : "8cb707e9-fe17-414c-b9c0-5468a88bc268"
        }
        self.uid = "fe9507a5-b526-4b57-97a4-df2ed1298a83"
        self.school = "73000001"
        self.ssion = session()
        # ssion.get("http://weiban.mycourse.cn/#/login",headers=self.header)

    def get_tasks(self):
        data = {
            "userId":     self.uid,
            "tenantCode": self.school,
            "limit" : 2
        }
        url = "https://weiban.mycourse.cn/pharos/index/listStudyTask.do?timestamp=1665650789"
        info = self.ssion.post(url, data=data,headers=self.header,verify = False)
        res = json.loads(info.text)['data']
        return res


    def get_category(self, userprojectid):
        url = "https://weiban.mycourse.cn/pharos/usercourse/listCategory.do?timestamp=1665652059"
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
        url = "https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp=1665652280"
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
        url1 = "https://weiban.mycourse.cn/pharos/usercourse/study.do"
        data = {
            "courseId":  courseid,
            "userProjectId": userprojectid,
            "tenantCode":    self.school,
            "userId":   self.uid
        }
        ans1 = self.ssion.post(url1, data=data,headers=self.header, verify = False)
        # print(ans1.text)
        
        url2 = "https://weiban.mycourse.cn/pharos/usercourse/getCourseUrl.do"
        ans2 = self.ssion.post(url2, data=data,headers=self.header, verify=False)
        # print(ans2.text)

        sleep(17)

        url3 = "https://weiban.mycourse.cn/pharos/usercourse/finish.do?userCourseId=" +  userCourseId + "&tenantCode="+ self.school
        ans3 = self.ssion.get(url3, headers=self.header, verify=False)
        print(ans3.text)

    def do_all(self):
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
                    print(course['resourceName'])
                    self.do_course(userProjectId, courseId, userCourseId)
                


if __name__ == '__main__':
    weike("320220927571").do_all()