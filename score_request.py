import urllib
import re
import requests
from bs4 import BeautifulSoup
from course import Course


class ScoreRequest:
    header = {
        'User-Agent': '''Mozilla/5.0 (Macfloatosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) 
                    Chrome/58.0.3029.110 Safari/537.36''',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': 1
    }

    login_url = "http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp"
    score_url = "http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2016-2017{}({})".format(
        urllib.parse.quote("学年第二学期", encoding='gbk'), urllib.parse.quote("两学期", encoding='gbk'))
    # score_url = "http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2016-2017%D1%A7%C4%EA%B5%DA%D2%BB%D1%A7%C6%DA(%C1%BD%D1%A7%C6%DA)"
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

    def __init__(self, student):
        self.student = student

    def request_score(self):
        """请求分数，存入student"""
        s = requests.Session()
        s.keep_alive = False

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
        return self.student.calc_average()

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
            print("Error, please check your student number or retry")
