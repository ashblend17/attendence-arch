import requests
from bs4 import BeautifulSoup
from pyjsparser import parse
import re
import json
import random
login_url = 'https://lms.iiitkottayam.ac.in/login/index.php'
# authenticated_url = 'https://lms.iiitkottayam.ac.in/some_authenticated_page'
session = requests.Session()
# session.cookies.set('MoodleSession','661j15q28glghusnnosq3hbnmv')
def try_login(session):

    login_response = session.get(login_url)
    soup = BeautifulSoup(login_response.text, 'html.parser')
    logintoken_input = soup.find('input', {'name': 'logintoken'})
    auth_data = {
        'logintoken' :logintoken_input.get('value'),
        'username': '',
        'password': '',
    }

    login_response = session.post(login_url, data=auth_data)
    # print(session.cookies.get('MoodleSession'))
    # write cookie to aa file
    # with open('cookie.txt', 'w') as f:
    #     f.write(session.cookies.get('MoodleSession'))
try_login(session)

# cookies = login_response.cookies
# session.cookies.update(cookies)

# soup = BeautifulSoup(login_response.text, 'html.parser')
# s = soup.find_all("script")

# search = re.search('"sesskey":"\w+',s[1].text)
# key = search.group(0)[len('"sesskey":"'):]
# print(s[1])
# print(key)
# https://lms.iiitkottayam.ac.in/lib/ajax/service.php?sesskey=2ygYcblMnh&info=core_course_get_enrolled_courses_by_timeline_classification
# data = '[{"index":0,"methodname":"core_course_get_enrolled_courses_by_timeline_classification","args":{"offset":0,"limit":24,"classification":"all","sort":"fullname","customfieldname":"","customfieldvalue":""}}]'
# x = json.loads(data)
# print(x)

# res = session.post("https://lms.iiitkottayam.ac.in/lib/ajax/service.php" , params={"sesskey" : key ,"info" :  "core_course_get_enrolled_courses_by_timeline_classification"} ,json=x)
# print(session.cookies)
# print(json.dumps(res.json()))


res = session.get('https://lms.iiitkottayam.ac.in/mod/attendance/view.php?id=11604&mode=1')

atten_soup = BeautifulSoup(res.text, 'html.parser')

rows = atten_soup.find_all('tr')[1:]
res = {}
for row in rows:
    C = row.find(class_='colcourse cell c0')
    if(C == None):
        continue
    Course = row.find(class_='colcourse cell c0').text
    Percentage = row.find(class_='colpercentagesessionscompleted').text
    if(Percentage == "-"):
        continue
    # course can be format
    # ICS123
    # 
    
    if("ICS123" not in Course and "Calculus" not in Course  ):
        num = -1
        try:
            # ICS 123
            num = int(Course.split(" ")[1])
        except:
            # ICS123
            num = int(Course.split(" ")[0]  [3:])
            
        if(num > 320):
            res[Course] = Percentage


    # print(Course.text,Percentage.text)

print(json.dumps(res))



# print(login_response.text)

# res = session.get(see)
# print(res.text)
# print(authenticated_soup)

session.close()

