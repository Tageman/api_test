import requests

def login():
    datap = {'email': '******', 'password': '****'}
    r = requests.post('************', data=datap)
    # print(r.json()['data']['token'])
    return r.json()['data']['token']

if __name__ == '__main__':
    login()
