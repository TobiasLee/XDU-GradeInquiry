import requests
from student import Student
import argparse

if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5

    parser = argparse.ArgumentParser(description='XDU GPA Inquiry')

    parser.add_argument(dest='id', metavar='student id')
    parser.add_argument(dest='pwd', metavar='password')

    parser.add_argument('-i', dest='course_info', action='store',
                        choices={'true', 'false'}, default='true',
                        help='display all course grade info')

    parser.add_argument('-avg', dest='avg_grade', action='store',
                        choices={'true', 'false'}, default='true',
                        help='display average grade')

    parser.add_argument('-g', dest='avg_gpa', action='store',
                        choices={'true', 'false'}, default= 'true',
                        help='display average gpa')

    parser.add_argument('-f', dest='filter_courses', nargs='*',
                        help="filter some courses you don't want to be calculated")

    args = parser.parse_args()
    student = Student(args.id, args.pwd)
    student.request_grade()
    if args.course_info == 'true':
        for course in student.courses:
            print(course.name, course.credit, course.score)

    if args.avg_grade == 'true':
        print("Average Grade (Including CET4 and CET6):")
        print(student.calc_average())

    if args.avg_gpa == 'true':
        print("Average GPA ( CET4 and CET6 not included):")
        print(student.calc_gpa(args.filter_courses))
