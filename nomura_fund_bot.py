import os
import datetime
import sys

import requests


def login(username, password):
    url = "https://wsapi.nomuradirect.com/ifundapi/api/v1/login"

    payload = {"username": username, "password": password}
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.json()


def buy(user_info, fund_code, amount):
    url = "https://wsapi.nomuradirect.com/ifundapi/api/v2/orders/buy"
    today = datetime.date.today()
    account0 = user_info['accounts'][0]
    account_number = account0['accountNumber']
    payload = {"entryBy": account_number,
               "fundCode": fund_code,
               "isSendOrder": "true",
               "ip": get_ip(),
               "bankCode": account0['ats'][0]['code'],
               "accountNumber": account_number,
               "amount": amount,
               "settleDate": today.strftime("%Y-%m-%d 09:00:00"),
               "payType": "A",
               "accountType": "O",
               "bankAccount": account0['ats'][0]['accountNumber']}

    headers = {
        'Authorization': user_info['token'],
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return response.json()


def get_estimate_nav(fund_code):
    url = "https://fundradars.stockradars.co/fundradars/v1.3/fund/realtime_nav"

    querystring = {"fund_id": fund_code}

    headers = {
        'Cache-Control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()


def get_ip():
    url = "http://httpbin.org/ip"

    headers = {
        'Cache-Control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)

    return response.json()['origin']


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python3 nomura_fund_bot.py <username> <password> <amount>')
        exit(-1)

    username_ = sys.argv[1]
    password_ = sys.argv[2]
    buy_amount = sys.argv[3]
    file = open(os.path.dirname(os.path.realpath(__file__)) + "/fund_list.txt", "r")
    fund_list = [i for i in file.read().splitlines()]
    buy_threshold = -1  # Change -1%
    user = login(username_, password_)
    for fund in fund_list:
        now_nav = get_estimate_nav(fund)
        # Buy when stock go down
        if now_nav['nav']['percent_change'] <= buy_threshold:
            print('BUY', fund, buy_amount)
            buy(user, fund, buy_amount)
