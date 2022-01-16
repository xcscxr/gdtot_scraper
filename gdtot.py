# TG@YukkiSenpai

import requests, re, base64

# file url
url = "" 
# add your crypt cookie here
crypt = "" 
# ==========================================

client = requests.Session()
client.cookies.update({ 'crypt': crypt })
res = client.get(url)

title = re.findall(">(.*?)<\/h5>", res.text)[0]
info = re.findall('<td\salign="right">(.*?)<\/td>', res.text)
res = client.get(f"https://new.gdtot.top/dld?id={url.split('/')[-1]}")

matches = re.findall('gd=(.*?)&', res.text)
decoded_id = base64.b64decode(str(matches[0])).decode('utf-8')
gdrive_url = f'https://drive.google.com/open?id={decoded_id}'

out = f'''
Title: {title}\nSize: {info[0]}\nDate: {info[1]}
Source URL: {url}\n\nGDrive-URL:\n{gdrive_url}
'''.strip()

print(out)
