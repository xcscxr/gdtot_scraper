import requests, re, base64

# file url
URL = "" 

# add your crypt cookie here
crypt = "" 

# ==========================================

def parse_info(res):
    title = re.findall(">(.*?)<\/h5>", res.text)[0]
    info = re.findall('<td\salign="right">(.*?)<\/td>', res.text)
    parsed_info = {
        'error': False,
        'title': title,
        'size': info[0],
        'date': info[1]
    }
    return parsed_info

# ==========================================

def gdtot_dl(url):
    client = requests.Session()
    client.cookies.update({ 'crypt': crypt })
    res = client.get(url)

    info = parse_info(res)
    info['src_url'] = url

    res = client.get(f"https://new.gdtot.top/dld?id={url.split('/')[-1]}")
    matches = re.findall('gd=(.*?)&', res.text)

    try:
        decoded_id = base64.b64decode(str(matches[0])).decode('utf-8')
        gdrive_url = f'https://drive.google.com/open?id={decoded_id}'
    except:
        info['error'] = True,
        return info

    info['gdrive_link'] = gdrive_url
    
    return info

# ==========================================

output = gdtot_dl(URL)

print(output)

# ==========================================
'''
SAMPLE OUTPUT:
{
    'error': False, 
    'title': 'Filename on website', 
    'size': '627.03 MB', 
    'date': '11-Feb-2022 02:47:12', 
    'src_url': 'https://gdtot-domain/file/XXX', 
    'gdrive_link': 'https://drive.google.com/open?id=XXXX...'
}
'''
