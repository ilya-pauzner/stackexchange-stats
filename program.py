import xml.etree.ElementTree as ET

def get_xml(name):
    return ET.parse(name).getroot()

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
good_guys.sort()
for elem in good_guys:
    print('User #', elem, ' <br>', sep = '', file = answer)
print('</body></html>', file = answer)
answer.close()