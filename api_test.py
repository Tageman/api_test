# -*- coding:utf-8 -*-

import xlrd
import json
import requests
import comm_login

# read file of excel_api
def read_excel(address):
    data = xlrd.open_workbook(address)
    table = data.sheets()[0]
    rows = table.nrows


    for i in range(1,rows):
        # list = str(table.row_values(i)).replace('u\'','\'')
        # print list.decode('unicode-escape')

        list = table.row_values(i)
        api_host = str(list[1].encode('utf-8'))
        request_url = str(list[2].encode('utf-8'))
        request_method = str(list[3].encode('utf-8'))
        request_data = str(list[4].encode('utf-8'))
        request_code = int(list[5])
        preview_code = int(list[6])

        # # 判断是什么类型在这里直接做处理
        # print(type(preview_code)) # float
        # print(type(api_host))   # unicode
        # print(type(request_url))   # unicode
        # print(type(request_code))  # float
        # print(type(request_data))   # unicode
        # print(type(request_method))  # unicode

        api_request(api_host,request_url,request_method,request_data,request_code,preview_code)


# api_request
def api_request(api_host,request_url,request_method,request_data,request_code,preview_code):

    token = ''.join(comm_login.login())

    headers = {'Content-Type': 'application/json',
               'Referer': 'http://' + api_host,
               'Authorization':token,
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

    # Judgment and request
    if request_method == 'POST':
        r = requests.post(api_host+request_url, headers=headers,data=request_data)

    elif request_method == 'GET':
        r = requests.get(api_host+request_url, headers=headers,params=request_data)

    elif request_method == 'PUT':
        r = requests.put(api_host+request_url, headers=headers,data=request_data)

    elif request_method == 'DELETE':
        r = requests.delete(api_host+request_url, headers=headers)

    elif request_method == 'PATCH':
        r = requests.patch(api_host+request_url, headers=headers,data=request_data)

    # The processing results
    if request_method != 'DELETE':
        if r.status_code == request_code and int(r.json()['code'].encode('utf-8')) == preview_code:
            print('this ok {0}'.format(api_host + request_url))
        else:
            print('this not ok {0}'.format(api_host + request_url))
    else:
        if r.status_code == request_code:
            print ('this ok {0}'.format(api_host + request_url))
        else:
            print ('this not ok {0}'.format(api_host + request_url))



def main():
    address = '/Users/ydz/Downloads/TestCase.xlsx'
    read_excel(address)

if __name__ == '__main__':
    main()





