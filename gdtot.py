import re
import base64
import requests
from urllib.parse import urlparse, parse_qs

# file url
URL = "" 

# add your crypt cookie here
crypt = "" 

# ==========================================

def parse_info(res):
    title = re.findall(">(.*?)<\/h5>", res.text)[0]
    info = re.findall('<td\salign="right">(.*?)<\/td>', res.text)
    parsed_info = {
        'error': True,
        'message': 'Link Invalid.',
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
    
    try:
        url = re.findall('URL=(.*?)"', res.text)[0]
    except:
        info['message'] = 'The requested URL could not be retrieved.',
        return info

    params = parse_qs(urlparse(url).query)
    
    if 'msgx' in params:
        info['message'] = params['msgx'][0]
    
    if 'gd' not in params or not params['gd'] or params['gd'][0] == 'false':
        return info
    
    try:
        decoded_id = base64.b64decode(str(params['gd'][0])).decode('utf-8')
        gdrive_url = f'https://drive.google.com/open?id={decoded_id}'
        info['message'] = 'Success.'
    except:
        info['error'] = True
        return info

    info['gdrive_link'] = gdrive_url
    
    return info
    
# ==========================================

info = gdtot_dl(URL)

print(info)

# ==========================================
'''
SAMPLE OUTPUT:
{
    'error': False,
    'message': 'Some status message..' 
    'title': 'Filename on website', 
    'size': '627.03 MB', 
    'date': '11-Feb-2022 02:47:12', 
    'src_url': 'https://gdtot-domain/file/XXX', 
    'gdrive_link': 'https://drive.google.com/open?id=XXXX...'
}
'''
