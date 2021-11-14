import random
import datetime
import json
import csv

name = ['Adobe Research Women-in-Technology Scholarship', 'Lounge Lizard Web Design Scholarship', 'Generation Google Scholarship', 'Elevate Women in Technology Scholarship', 'abc', 'xyz', 'def']

def randomName():
    return randomArray(name)

desc = ['These scholarships are open to female undergraduate and master’s students studying artificial intelligence/machine learning, data science, computer science or mobile/web development at North American universities, including Canada and Mexico', 
    'These scholarships are open to female undergraduate and master’s students studying artificial intelligence/machine learning, data science, computer science or mobile/web development at North American universities, including Canada and Mexico',
    'Open to all high school seniors and college students who excel in technology. Historically underrepresented  groups, such as Black/African American, Hispanic/Latinx, American Indian, or Native Hawaiian/Pacific Islander students are especially encouraged to apply',
    'High school seniors, college students, and graduate students who are or planning on studying STEM',
    'Open to military veterans and their families (age 16 and over) pursuing an undergraduate or graduate degree related to technology',
    'High school seniors, college students, and graduate students who are planning on studying STEM (international students are welcome to apply)']
def randomDesc():
    return randomArray(desc)

def randomArray(list):
    return list[random.randrange(0, len(list))]

end = datetime.datetime(2022, 9, 1)
start = datetime.datetime(2020, 1, 1)
def randomDate():
    return random.random() * (end - start) + start

prize_range = (1000, 1000000)
def randomPrize():
    return random.randrange(prize_range[0], prize_range[1])

def randomize(list):
    l = []
    for i in list:
        l.append({"link": i, "name": randomName(), "due_date": randomDate(), "desc": randomDesc(), "prize": randomPrize()})
    return l     

if __name__ == '__main__':
    data = json.load(open('list.txt', 'r'))
    with open('list.csv', 'w') as w:
        for (_, links) in data.items():
            w.write('\"{}\",\"{}\",\"{}\",\"{}\"\n'.format(randomName(), randomDate(), randomDesc(), randomPrize()))
     
