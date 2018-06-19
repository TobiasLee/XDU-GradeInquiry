# -*- coding=utf-8 -*-
import requests
from score_request import *
from util import *


class Student:
    def __init__(self, id, password):
        self.average = 0
        self.courses = []
        self.id = id
        self.password = password

    def add_course(self, course):
        self.courses.append(course)

    def calc_average(self):
        if self.courses:
            credit_sum = 0
            average_grade = 0
            for course in self.courses:
                try:
                    grade = float(course.score)
                except ValueError:
                    continue
                course_credit = float(course.credit)
                credit_sum += course_credit
                average_grade += grade * course_credit
            if credit_sum == 0:
                return "Error, Please Retry!"
            else:
                return average_grade / credit_sum
        else:
            self.request_grade()
            self.calc_average()

    def request_grade(self):
        '''request grade information through ScoreRequest Object'''
        score_request = ScoreRequest(self)
        return score_request.request_score()

    @staticmethod
    def score2gpa(s):
        ''' get corresponding gpa for score, s is a float'''
        if s >= 95:
            return 4.0
        elif s >= 90:
            return 3.9
        elif s >= 84:
            return 3.8
        elif s >= 80:
            return 3.6
        elif s >= 76:
            return 3.4
        elif s >= 73:
            return 3.2
        elif s >= 70:
            return 3.0
        elif s >= 67:
            return 2.7
        elif s >= 64:
            return 2.4
        elif s >= 62:
            return 2.2
        elif s >= 60:
            return 2.0
        else:
            return 0.0

    def get_course_info(self):
        '''return courses info pair '''
        c_name = []
        c_score = []
        c_credit = []
        for c in self.courses:
            c_name.append(c.name)
            c_score.append(c.score)
            c_credit.append(c.credit)
        return zip(c_name, c_credit, c_score)

    def calc_gpa(self, filters=None):
        total_credit = 0
        total_gpa = 0
        course_info = list(self.get_course_info())
        if filters:
            for keyword in filters:
                course_info = course_filter(course_info, keyword)

        for n, c, s in course_info:
            if n.find('四级') != -1 or n.find('六级') != -1:
                continue
            total_credit += float(c)
            if s == '通过' or s == '中等':
                total_gpa += float(c) * 3.2
            elif s == '优秀':
                total_gpa += float(c) * 4.0
            elif s == '不通过' or s == '不及格':
                total_credit += 0
            elif s == '良好':
                total_gpa += float(c) * 3.8
            elif s == '及格' or s == '免修':
                total_gpa += float(c) * 2.4
            else:
                total_gpa += float(c) * self.score2gpa(float(s))
        return total_gpa / total_credit









