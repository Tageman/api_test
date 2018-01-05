import requests

def login():
    datap = {'email': 'r3answer@163.com', 'password': 'qn123456'}
    r = requests.post('http://deve.qingniux.com/enterprise/operator/login', data=datap)
    # print(r.json()['data']['token'])
    return r.json()['data']['token']

if __name__ == '__main__':
    login()