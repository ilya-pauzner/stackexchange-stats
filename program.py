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

tags = get_xml('Tags.xml')
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
        
posts = get_xml('Posts.xml')
lotr_users = set()
harry_users = set()
starwars_users = set()

posts_dict = dict()
for elem in posts:
    posts_dict[elem.attrib['Id']] = elem

for elem in posts:
    if 'OwnerUserId' in elem.attrib:
        user_id = elem.attrib['OwnerUserId']
    if elem.attrib['PostTypeId'] in ('1', '2'):
        j = 0
        while 'ParentId' in elem.attrib:
            elem = posts_dict[elem.attrib['ParentId']]
        if elem.attrib['PostTypeId'] == '1':
            parse_question(elem, user_id)
            
good_guys = []
for elem in sorted(lotr_users):
    if elem in harry_users and (not elem in starwars_users):
        good_guys.append(int(elem))

answer = open('output.html', 'w')
print('<html><head><title> Stats </title></head><body><h3> Here are users who participated in Lord of the Rings and Harry Potter sections, but did not participate in the Star wars section </h3><br>', file = answer) 
print('<table border = "1px solid black">', file = answer)
print('<th> Name </th> <th> Id </th>', file = answer)
users = get_xml('Users.xml')
users_dict = dict()
for elem in users:
    users_dict[elem.attrib['Id']] = elem
    
for i in range(len(good_guys)):
    good_guys[i] = [users_dict[str(good_guys[i])].attrib['DisplayName'], good_guys[i]]
    
good_guys.sort()

for elem in good_guys:
    t = elem[0]
    elem[0] = ''
    for letter in t:
        if letter in string.ascii_letters:
            elem[0] += letter
    print('<tr> <td>', elem[0], '</td> <td>', elem[1] ,'</td> </tr>', file = answer)

print('</table></body></html>', file = answer)
answer.close()
