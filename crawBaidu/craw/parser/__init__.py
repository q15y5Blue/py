import datetime
import re
def getTime(timeStr):
    todays =str(datetime.datetime.now().date())
    toyearStr = str(datetime.datetime.now().year)
    if '今天' in timeStr:
        timeStr = timeStr.replace("今天", todays)
    todayRe = re.compile('\d{1,2}:\d\d')
    monthRe = re.compile('\d{1,2}-\d{1,2}.*\d\d:\d\d')
    yearRe = re.compile('\d{1,4}-\d{1,2}-\d{1,2}.*\d\d:\d\d')
    if (todayRe.match(timeStr)):
        dateStr = todays + ' ' + timeStr
        return dateStr
    elif monthRe.match(timeStr):
        dataStr = toyearStr+"-"+str(timeStr)
        return dataStr
    elif yearRe.match(timeStr):
        return timeStr

# if __name__ =='__main__':
#     strs = "1-3 18:32"
#     print(getTime(strs))