import requests
from bs4 import BeautifulSoup
import re
import urllib


class Student:
    def __init__(self, id, password):
        self.average = 0
        self.courses = []
        self.id = id
        self.password = password

    def add_course(self, course):
        self.courses.append(course)

    def calc_average(self, school_year, term):
        """计算均分 输入学年 学期 eg: calc_average(2016, 2) 2016学年第2学期"""
        credit_sum = 0
        average_grade = 0
        if self.courses:
            for course in self.courses:
                try:
                    grade = float(course.score)
                except ValueError:
                    continue
                course_credit = float(course.credit)
                credit_sum += course_credit
                average_grade += grade * course_credit
            if credit_sum == 0:
                print("Error, Please Retry!")
            else:
                print("Average:", average_grade / credit_sum)
        else:
            self.request_grade(school_year, term)
            self.calc_average(school_year, term)

    def request_grade(self, school_year, term):
        score_request = ScoreRequest(self, school_year, term)
        score_request.request_score()


class Course:
    """课程类"""
    def __init__(self, name, credit):
        self.name = name
        self.credit = credit
        self.score = 0

    def set_score(self, score):
         self.score = score


class ScoreRequest:
    """请求 封装类"""
    header = {
    'User-Agent': '''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) 
                    Chrome/58.0.3029.110 Safari/537.36''',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': 1
    }

    login_url = "http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp"
    post_data = {
        'username': '',
        'password': '',
        'submit': '',
        'lt': '',
        'dllt': "userNamePasswordLogin",
        "captchaResponse": "",
        'execution': 'e1s1',
        '_eventId': 'submit',
        'rmShown': '1'
    }

    def __init__(self, student, school_year, term):
        self.student = student
        self.score_url = "http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm={}-{}{}({})".\
            format(school_year, school_year+1, urllib.parse.quote("学年第{}学期".format("一" if term == 1 else "二"), encoding='gbk'), urllib.parse.quote("两学期", encoding='gbk'))


    def request_score(self):
        """请求分数，存入student"""
        s = requests.Session()
        r = s.get(self.login_url)
        html = r.text
        lt = re.findall(r'value="LT.*"', html)[0]
        lt = lt[7:-1]

        self.post_data['username'] = self.student.id
        self.post_data['password'] = self.student.password
        self.post_data['lt'] = lt

        # 登陆
        s.post(self.login_url, self.post_data)
        # 查询成绩
        res = s.get(self.score_url)
        scores_page = res.text
        self.handle_score_page(scores_page)

    def handle_score_page(self, scores_page):
        """处理分数页面 把结果保存到student的courses数组中"""
        bs_obj = BeautifulSoup(scores_page, 'html5lib')
        course_tags = bs_obj.find_all('tr', attrs={'class': "odd"})
        score_tags = bs_obj.find_all('p')
        if course_tags:
            for course_tag in course_tags:
                course_name = course_tag.contents[5].contents[0].strip()
                course_credit = course_tag.contents[9].contents[0].strip()
                c = Course(course_name, course_credit)
                self.student.courses.append(c)
            for score, course in zip(score_tags, self.student.courses):
                grade = score.contents[0].strip()
                course.set_score(grade)
        else:
            print("Error in hanle score pages")


if __name__ == '__main__':
    student = Student("学号", "密码")
    student.request_grade(2016, 2)
    for course in student.courses:
        print(course.name, course.credit, course.score)
    student.calc_average(2016, 2)