import requests

def login():
    datap = {'email': 'youremail', 'password': 'yourpassword'}
    r = requests.post('****login address', data=datap)
    # print(r.json()['data']['token'])
    return r.json()['data']['token']

if __name__ == '__main__':
    login()
