import xml.etree.ElementTree
import string

def get_xml(name):
    return xml.etree.ElementTree.parse(name).getroot()


def have_any(substrings, string):
    for elem in substrings:
        if elem in string:
            return True
    return False


def parse_question(elem, user_id):
    if have_any(lotr, elem.attrib['Tags']):
        lotr_users.add(user_id)
    if have_any(harry, elem.attrib['Tags']):
        harry_users.add(user_id)    
    if have_any(starwars, elem.attrib['Tags']):
        starwars_users.add(user_id)  
        
        
def parse_comment(elem, user_id):
    elem = posts_dict[elem.attrib['PostId']]
    if elem.attrib['PostTypeId'] in ('1', '2'):
        while 'ParentId' in elem.attrib:
            elem = posts_dict[elem.attrib['ParentId']]
        if elem.attrib['PostTypeId'] == '1':
            parse_question(elem, user_id)
            

def open_files_and_process_them():
    global posts, posts_dict
    posts = get_xml('Posts.xml')
    posts_dict = dict()
    for elem in posts:
        posts_dict[elem.attrib['Id']] = elem    

    global users, users_dict
    users = get_xml('Users.xml')
    users_dict = dict()
    for elem in users:
        users_dict[elem.attrib['Id']] = elem    
    
    global comments
    comments = get_xml('Comments.xml')
    
    global tags
    tags = get_xml('Tags.xml')
    

def print_output():
    answer = open('output.html', 'w', encoding = 'utf-8')
    print('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">', file = answer)
    print('<html><head><title> Stats </title></head><body><h3> Here are users who participated in Lord of the Rings and Harry Potter sections, but did not participate in the Star wars section </h3><br>', file = answer) 
    print('<table border = "1px solid black">', file = answer)
    print('<th> Name </th> <th> Id </th>', file = answer)    
    for i in range(len(good_guys)):
        print('<tr> <td>', good_guys[i][0], '</td> <td>', good_guys[i][1] ,'</td> </tr>', file = answer)
    print('</table></body></html>', file = answer)
    answer.close()    
    

open_files_and_process_them()


lotr = []
harry = []
starwars = []
for elem in tags:
    if 'lord-of-the-rings' in  elem.attrib['TagName']:
        lotr.append(elem.attrib['TagName'])
    if 'harry-potter' in  elem.attrib['TagName']:
        harry.append(elem.attrib['TagName'])
    if 'star-wars' in  elem.attrib['TagName']:
        starwars.append(elem.attrib['TagName'])
        
        
lotr_users = set()
harry_users = set()
starwars_users = set()
for elem in posts:
    if 'OwnerUserId' in elem.attrib:
        user_id = elem.attrib['OwnerUserId']
    if elem.attrib['PostTypeId'] in ('1', '2'):
        while 'ParentId' in elem.attrib:
            elem = posts_dict[elem.attrib['ParentId']]
        if elem.attrib['PostTypeId'] == '1':
            parse_question(elem, user_id)                          
for elem in comments:
    if 'UserId' in elem.attrib:
        user_id = elem.attrib['UserId']
        parse_comment(elem, user_id)
        
            
good_guys = []
for elem in lotr_users:
    if elem in harry_users and (not elem in starwars_users):
        good_guys.append(elem)
for i in range(len(good_guys)):
    good_guys[i] = [users_dict[good_guys[i]].attrib['DisplayName'], good_guys[i]]
good_guys.sort()


print_output()
