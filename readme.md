# Nomura Fund Bot
Bot for auto buy fund base on underling stock value change for Nomura iFund (Thailand).

## Features

- Auto buy on funds from realtime underlying stock value drop on a threshold like (2%).

## Getting start

- Require Python3
- Download or clone this code.
- Install dependencies

```
pip install -r requirements.txt
```

- Change enable fund list on file 'fund_list.txt', please make sure it is the Thai equity fund only.
- Setting crontab for run automatic on 12.33 Mon-Fri(My computer using UTC time it will be 5:33).
For example
Username: MyUserName 
Password: MyPassWord
amount: ฿1000

```
33 5 * * 1-5 python3 /path/to/code/nomura_fund_bot/nomura_fund_bot.py MyUserName MyPassWord 1000
```
