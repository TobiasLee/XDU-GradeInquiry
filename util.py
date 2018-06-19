def course_filter(info, keyword):
    info_filtered = [i for i in info if i[0].find(keyword) == -1]
    return info_filtered