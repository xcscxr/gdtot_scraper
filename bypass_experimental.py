import requests
from lxml import html

url = 'https://new.gdtot.zip/file/1234567890'

# ---------------------------------------------

api = 'https://5e04.uuxd.workers.dev'
api_res = requests.get(api, params={
    'url': url
}).text

tree = html.fromstring(api_res)
tg = tree.xpath("//button[@id='dirdown']/@onclick")[0][7:-2]

# ---------------------------------------------

forms = tree.xpath('//form')
ddl = forms[0]
ddlu = ddl.xpath("./@action")[0]
form_data = {}
for input_element in ddl.xpath('.//input'):
    name = input_element.get("name")
    value = input_element.get("value")
    form_data[name] = value

res = requests.post(ddlu, data=form_data).text
tree = html.fromstring(res)
drive = tree.xpath('//button[@onclick]/@onclick')[0][6:-2]

# ---------------------------------------------

print({'tg': tg, 'drive': drive})


'''
    sample op:
{
    'tg': 'https://t.me/FilestoringmBot?start=M-y-Z-a-xyzabc-xyzabc-', 
    'drive': 'https://drive.google.com/u/0/uc?id=1234567890abcdefghijklm1234567890&export=download'
}
'''
