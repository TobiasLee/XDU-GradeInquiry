# XDU 成绩查询
## 说明

XDU 均分和 GPA 查询爬虫，不用评教也能查成绩算 GPA 啦~

## 环境要求

- Python 3

- requests

- BeautifulSoup

你可以使用 `pip3 install` 来安装需要的库

## 使用教程

在命令行输入：

> python3 main.py 你的学号 你的密码 

就能查目前所有科目的成绩以及计算均分和 GPA（采用最新[算法](http://liuxue.xidian.edu.cn/info/1002/2482.htm)）

可选参数：

> optional arguments:
>
>   -h, --help            show this help message and exit
>
>   -i {false,true}       display all course grade info
>
>   -avg {false,true}     display average grade
>
>   -g {false,true}       display average gpa
>
>   -f [FILTER_COURSES [FILTER_COURSES ...]]
>
> ​                        filter some courses you don't want to be calculated

其中：-f 参数可以指定你**不想**计算课程的关键字，你可以使用`-f 英语`来过滤过所有英语课程，`-f 英语 体育` 来过滤掉英语和体育所有课程。

更多帮助请使用 `python3 main.py -h` 查看


