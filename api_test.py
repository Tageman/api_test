# -*- coding:utf-8 -*-

import xlrd
import requests
import comm_login
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# read file of excel_api
def read_excel(address):
    data = xlrd.open_workbook(address)
    table = data.sheets()[0]
    rows = table.nrows


    for i in range(1,rows):
        # list = str(table.row_values(i)).replace('u\'','\'')
        # print list.decode('unicode-escape')

        list = table.row_values(i)
        api_host = str(list[1].encode('utf-8')).strip()
        request_url = str(list[2].encode('utf-8')).strip()
        request_method = str(list[3].encode('utf-8')).strip()
        request_data = str(list[4].encode('utf-8')).strip()
        request_code = int(list[5])

        if list[6] == '':
            preview_code = list[6]
        else:
            preview_code = int(list[6])

        # # 判断是什么类型在这里直接做处理
        # print(type(preview_code)) # float
        # print(type(api_host))   # unicode
        # print(type(request_url))   # unicode
        # print(type(request_code))  # float
        # print(type(request_data))   # unicode
        # print(type(request_method))  # unicode

        api_request(api_host,request_url,request_method,request_data,request_code,preview_code)
    return send_email()

# 执行读取完毕后发送邮件
def send_email():

    sender = 'youemail'
    password = 'youemailpasswrod'
    receivers = 'receemail'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receivers
    msg['Subject'] = 'API_Test_Result'

    msg.attach(MIMEText('当前接口测试结果（结果全部显示在附件中）', 'plain', 'utf-8'))

    att1 = MIMEText(open('result.txt', 'rb').read(), 'base64', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'
    att1['Content-Disposition'] = 'attahment; filename="result.txt"'
    msg.attach(att1)

    smtpobj = smtplib.SMTP('smtp.139.com', 25)
    smtpobj.login(sender, password)
    smtpobj.sendmail(sender, receivers, msg.as_string())
    smtpobj.quit()

# 执行写文件（将结果写到文件中，并最后执行邮件）
def write_file(request_result):
    with open('result.txt', 'a+') as file:
        file.write(request_result + '\n')



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
            return write_file('this ok {0}'.format(api_host + request_url))
        else:
            print('this not ok {0}'.format(api_host + request_url))
            return write_file('this not ok {0}'.format(api_host + request_url))
    else:
        if r.status_code == request_code:
            print ('this ok {0}'.format(api_host + request_url))
            return write_file('this ok {0}'.format(api_host + request_url))
        else:
            print ('this not ok {0}'.format(api_host + request_url))
            return write_file('this not ok {0}'.format(api_host + request_url))



def main():
    address = '/Users/ydz/Downloads/TestCase1.xlsx'
    read_excel(address)

if __name__ == '__main__':
    main()





